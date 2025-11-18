# -*- coding: latin-1 -*-
from datetime import date, datetime
import calendar
import holidays
from dateutil.relativedelta import relativedelta
"""
    - Created By: Delvidio Demarchi Neto
    - Created Date: 03/04/2023
    - Laste Update: 18/11/2025
    - Version: '2.0.0'
"""


class intdate():
    """Classe para manipulação e incremento de datas.
    
    Permite incrementar/decrementar datas por ano, mês, dia ou dia útil,
    com suporte a calendário normal ou fiscal (4-4-5).
    
    Args:
        Interval (str): Tipo de intervalo. Valores: 'YEAR', 'MONTH', 'DAY', 'BDAY'.
        Date (date ou str): Data de referência no formato 'YYYY-MM-DD'.
        Increment (int): Número de intervalos a incrementar (pode ser negativo).
        Alignment (str): Alinhamento da data. Valores: 'B' (início), 'E' (fim), 'S' (mesmo dia).
        Country (str, optional): Código do país para cálculo de dias úteis (obrigatório se Interval='BDAY').
        State (str, optional): Código do estado/província para cálculo de dias úteis.
        Weekend (bool, optional): Se False, sábado não é dia útil. Se True, apenas domingo não é dia útil.
        CalendarType (str, optional): Tipo de calendário. Valores: 'NORMAL' (padrão) ou 'FISCAL' (4-4-5).
    
    Examples:
        >>> from bonniebully import intdate
        >>> from datetime import date
        >>> 
        >>> # Incrementar 3 meses
        >>> result = intdate('MONTH', date(2024, 1, 15), 3, 'S').getDates()
        >>> 
        >>> # Calcular 5 dias úteis
        >>> result = intdate('BDAY', date(2024, 1, 15), 5, 'S', 'BR', 'SP').getDates()
    """

    def __init__(self, Interval: str, Date: date, Increment: int,
                 Alignment: str, Country: str = "", State: str = "", Weekend: bool = False,
                 CalendarType: str = "NORMAL"):

        # Validação de parâmetros
        if not isinstance(Interval, str):
            raise TypeError("Interval deve ser uma string")
        if not isinstance(Increment, int):
            raise TypeError("Increment deve ser um número inteiro")
        if Alignment.upper() not in ["B", "E", "S"]:
            raise ValueError("Alignment deve ser 'B', 'E' ou 'S'")
        if Interval.upper() not in ["YEAR", "MONTH", "DAY", "BDAY"]:
            raise ValueError("Interval deve ser 'YEAR', 'MONTH', 'DAY' ou 'BDAY'")
        if Interval.upper() == "BDAY" and not Country:
            raise ValueError("Country é obrigatório quando Interval é 'BDAY'")
        if CalendarType.upper() not in ["NORMAL", "FISCAL"]:
            raise ValueError("CalendarType deve ser 'NORMAL' ou 'FISCAL'")

        self._Interval = Interval
        self._Increment = Increment
        self._Alignment = Alignment
        self._Country = Country  # Corrigido: era _Contry
        self._State = State
        self._Weekend = Weekend
        self._CalendarType = CalendarType.upper()
        self._EndDate = ''

        if isinstance(Date, str) is True:
            self._Date = datetime.strptime(Date, '%Y-%m-%d')
        else:
            self._Date = datetime.combine(Date, datetime.min.time())

    def getDates(self) -> date:
        """Retorna a data calculada baseada nos parâmetros fornecidos.
        
        Returns:
            date: Data resultante do cálculo de incremento/decremento.
        """

        vDayClass = self._Date.day

        def __getLastMondayOfMonth(year: int, month: int) -> date:
            """Retorna a última segunda-feira do mês.
            
            Args:
                year: Ano.
                month: Mês (1-12).
            
            Returns:
                date: Última segunda-feira do mês especificado.
            """
            # Último dia do mês
            if month == 12:
                last_day = date(year, 12, 31)
            else:
                last_day = date(year, month + 1, 1) - relativedelta(days=1)
            
            # Encontra a última segunda-feira do mês
            if last_day.weekday() == 0:
                return last_day
            else:
                days_back = last_day.weekday()
                return last_day - relativedelta(days=days_back)

        def __getLastCompleteWeekMonday(year: int, month: int) -> date:
            """Retorna a última segunda-feira do mês onde a semana está completa.
            
            Semana completa: segunda a domingo, todos os dias dentro do mês.
            
            Args:
                year: Ano.
                month: Mês (1-12).
            
            Returns:
                date: Última segunda-feira onde a semana completa está dentro do mês.
            """
            # Último dia do mês
            if month == 12:
                last_day = date(year, 12, 31)
            else:
                last_day = date(year, month + 1, 1) - relativedelta(days=1)
            
            # Encontra a última segunda-feira do mês
            if last_day.weekday() == 0:
                last_monday = last_day
            else:
                days_back = last_day.weekday()
                last_monday = last_day - relativedelta(days=days_back)
            
            # Verifica se a semana está completa (domingo ainda está no mês)
            week_end = last_monday + relativedelta(days=6)  # Domingo da semana
            
            # Se o domingo não está no mesmo mês, retrocede uma semana
            # A última semana completa: domingo é o último dia do mês
            if week_end.month != month or week_end.year != year:
                last_monday = last_monday - relativedelta(weeks=1)
            
            return last_monday

        def __getLastCompleteWeekSunday(year: int, month: int) -> date:
            """Retorna o domingo da última semana completa do mês.
            
            Args:
                year: Ano.
                month: Mês (1-12).
            
            Returns:
                date: Domingo da última semana completa do mês.
            """
            last_monday = __getLastCompleteWeekMonday(year, month)
            return last_monday + relativedelta(days=6)  # Domingo da semana

        def __getFiscalYearStart(year: int) -> date:
            """Retorna a data de início do ano fiscal.
            
            O ano fiscal N começa na última segunda-feira de novembro do ano N-1
            onde a semana está completa.
            
            Args:
                year: Ano fiscal.
            
            Returns:
                date: Data de início do ano fiscal (última segunda-feira de novembro do ano anterior).
            """
            return __getLastCompleteWeekMonday(year - 1, 11)

        def __getFiscalMonthInfo(fiscal_year_start: date, fiscal_month: int, fiscal_year: int):
            """Retorna início e fim de um mês fiscal.
            
            Cada mês fiscal começa na segunda-feira e termina no domingo.
            O mês fiscal 1 começa na última segunda-feira de dezembro (se dia >= 28)
            ou na primeira segunda-feira de janeiro. O mês fiscal 12 termina no
            primeiro domingo de janeiro do ano seguinte que fecha semana completa.
            
            Args:
                fiscal_year_start: Data de início do ano fiscal.
                fiscal_month: Mês fiscal (1-12).
                fiscal_year: Ano fiscal.
            
            Returns:
                tuple: (data_início, data_fim) do mês fiscal.
            """
            if fiscal_month == 1:
                # Mês fiscal 1: começa na última segunda-feira de dezembro do ano anterior
                # OU na primeira segunda-feira de janeiro, a que for mais próxima do início do ano
                # Encontra a última segunda-feira de dezembro (não necessariamente onde semana está completa)
                dec_last = date(fiscal_year - 1, 12, 31)
                if dec_last.weekday() == 0:
                    dec_last_monday = dec_last
                else:
                    days_back = dec_last.weekday()
                    dec_last_monday = dec_last - relativedelta(days=days_back)
                
                jan_first = date(fiscal_year, 1, 1)
                
                # Calcula a primeira segunda-feira de janeiro
                if jan_first.weekday() == 0:
                    jan_first_monday = jan_first
                else:
                    days_to_monday = (7 - jan_first.weekday()) % 7
                    if days_to_monday == 0:
                        days_to_monday = 7
                    jan_first_monday = jan_first + relativedelta(days=days_to_monday)
                
                # Regra: se 1º de janeiro é segunda-feira, usa ele
                # Caso contrário, usa a última segunda-feira de dezembro se ela estiver em 28, 29, 30 ou 31 de dezembro
                # Senão usa a primeira segunda-feira de janeiro
                if jan_first.weekday() == 0:
                    # 1º de janeiro é segunda-feira, usa ele
                    month_start = jan_first
                else:
                    # Verifica se a última segunda-feira de dezembro está no final de dezembro (28-31)
                    if dec_last_monday.day >= 28:
                        # Última segunda-feira de dezembro está no final do mês, usa ela
                        month_start = dec_last_monday
                    else:
                        # Usa a primeira segunda-feira de janeiro
                        month_start = jan_first_monday
                
                # Termina no último domingo de janeiro
                month_end = __getLastCompleteWeekSunday(fiscal_year, 1)
                
            elif fiscal_month == 12:
                # Mês fiscal 12: começa na última segunda-feira de novembro onde a semana está completa
                month_start = __getLastCompleteWeekMonday(fiscal_year, 11)
                
                # Termina no primeiro domingo de janeiro do ano seguinte que fecha uma semana completa
                # a partir do início do mês 12
                jan_first = date(fiscal_year + 1, 1, 1)
                
                # Encontra o primeiro domingo de janeiro
                if jan_first.weekday() == 6:  # Domingo
                    first_sunday = jan_first
                else:
                    days_to_sunday = (6 - jan_first.weekday()) % 7
                    if days_to_sunday == 0:
                        days_to_sunday = 7
                    first_sunday = jan_first + relativedelta(days=days_to_sunday)
                
                # Verifica se o primeiro domingo de janeiro fecha uma semana completa
                days_diff = (first_sunday - month_start).days
                if (days_diff + 1) % 7 == 0:  # Fecha semana completa
                    month_end = first_sunday
                else:
                    # Não fecha, vai até o próximo domingo
                    month_end = first_sunday + relativedelta(weeks=1)
                    
            else:
                # Meses fiscais 2-11: mapeia para meses calendário
                # Mês fiscal 2 = janeiro, 3 = fevereiro, ..., 11 = outubro
                calendar_month = fiscal_month - 1
                
                # Início: última segunda-feira do mês calendário correspondente
                # Mês fiscal 2 começa na última segunda-feira de janeiro
                # Mês fiscal 3 começa na última segunda-feira de fevereiro
                # etc.
                month_start = __getLastMondayOfMonth(fiscal_year, calendar_month)
                
                # Fim: último domingo do mês calendário seguinte
                # Mês fiscal 2 termina no último domingo de fevereiro
                # Mês fiscal 3 termina no último domingo de março (ou primeiro domingo de abril)
                next_calendar_month = calendar_month + 1
                if next_calendar_month > 12:
                    next_calendar_month = 1
                    next_calendar_year = fiscal_year + 1
                else:
                    next_calendar_year = fiscal_year
                
                month_end = __getLastCompleteWeekSunday(next_calendar_year, next_calendar_month)
                
                # Verifica se fecha uma semana completa
                # Para fechar semana completa (segunda a domingo), (days + 1) deve ser múltiplo de 7
                days_diff = (month_end - month_start).days
                if (days_diff + 1) % 7 != 0:  # Não fecha semana completa
                    # Vai até o primeiro domingo do mês seguinte seguinte
                    if next_calendar_month == 12:
                        next_next_month = 1
                        next_next_year = next_calendar_year + 1
                    else:
                        next_next_month = next_calendar_month + 1
                        next_next_year = next_calendar_year
                    
                    next_next_month_first = date(next_next_year, next_next_month, 1)
                    if next_next_month_first.weekday() == 6:  # Domingo
                        first_sunday = next_next_month_first
                    else:
                        days_to_sunday = (6 - next_next_month_first.weekday()) % 7
                        if days_to_sunday == 0:
                            days_to_sunday = 7
                        first_sunday = next_next_month_first + relativedelta(days=days_to_sunday)
                    
                    # Verifica se esse domingo fecha uma semana completa
                    days_diff2 = (first_sunday - month_start).days
                    if (days_diff2 + 1) % 7 == 0:
                        month_end = first_sunday
                    else:
                        # Ainda não fecha, vai até o próximo domingo
                        month_end = first_sunday + relativedelta(weeks=1)
            
            return month_start, month_end

        def __getFiscalMonthFromDate(vDate: date) -> tuple:
            """Determina o ano e mês fiscal para uma data.
            
            Args:
                vDate: Data a ser analisada.
            
            Returns:
                tuple: (ano_fiscal, mês_fiscal) onde mês_fiscal é 1-12.
            """
            year = vDate.year
            month = vDate.month
            
            # Tenta determinar o ano fiscal testando anos próximos
            # O ano fiscal N começa em novembro do ano N-1
            for test_year in [year - 1, year, year + 1]:
                fiscal_year_start = __getFiscalYearStart(test_year)
                # Calcula o fim do ano fiscal (mês 12)
                month12_start, month12_end = __getFiscalMonthInfo(fiscal_year_start, 12, test_year)
                
                if fiscal_year_start <= vDate <= month12_end:
                    fiscal_year = test_year
                    # Agora determina qual mês fiscal
                    # Testa cada mês fiscal
                    for test_month in range(1, 13):
                        month_start, month_end = __getFiscalMonthInfo(fiscal_year_start, test_month, fiscal_year)
                        if month_start <= vDate <= month_end:
                            return fiscal_year, test_month
                    # Se não encontrou, retorna o mês 12
                    return fiscal_year, 12
            
            # Se não encontrou em nenhum ano, assume o ano atual
            # e tenta determinar o mês baseado no mês calendário
            fiscal_year = year
            if month == 11 or month == 12:
                # Novembro ou dezembro podem ser mês 1 ou 12
                # Verifica qual
                fiscal_year_start = __getFiscalYearStart(year)
                month1_start, month1_end = __getFiscalMonthInfo(fiscal_year_start, 1, year)
                if month1_start <= vDate <= month1_end:
                    return year, 1
                else:
                    return year, 12
            elif month == 1:
                # Janeiro pode ser mês 2 ou 3
                fiscal_year_start = __getFiscalYearStart(year)
                month2_start, month2_end = __getFiscalMonthInfo(fiscal_year_start, 2, year)
                if month2_start <= vDate <= month2_end:
                    return year, 2
                else:
                    return year, 3
            else:
                # Meses 2-10: mês fiscal = mês calendário + 2
                # (fevereiro = mês fiscal 4, março = 5, etc.)
                fiscal_month = month + 2
                if fiscal_month > 12:
                    fiscal_month = 12
                return year, fiscal_month

        def __getAlignment(vYearMeth: int, vMonthMeth: int, vDayMeth: int):
            """Aplica o alinhamento à data.
            
            Args:
                vYearMeth: Ano.
                vMonthMeth: Mês.
                vDayMeth: Dia.
            
            Returns:
                date: Data com alinhamento aplicado ('B', 'E' ou 'S').
            """

            if self._Alignment.upper() == "B":
                vDateMeth = date(vYearMeth, vMonthMeth, 1)

            elif self._Alignment.upper() == "S":
                # Garante que o dia existe no mês (ex: 31 de jan -> 28/29 de fev)
                endOfMonth = calendar.monthrange(vYearMeth, vMonthMeth)
                safeDay = min(vDayMeth, endOfMonth[1])
                vDateMeth = date(vYearMeth, vMonthMeth, safeDay)

            elif self._Alignment.upper() == "E":
                endOfMonth = calendar.monthrange(vYearMeth, vMonthMeth)
                vDateMeth = date(vYearMeth, vMonthMeth, endOfMonth[1])
            return vDateMeth

        def __checkNegative(value: int):
            """Verifica se um valor é negativo.
            
            Args:
                value: Valor a verificar.
            
            Returns:
                bool: True se negativo, False caso contrário.
            """
            if value < 0:
                check = True
            else:
                check = False
            return check

        def __getYear():
            """Calcula a data incrementando/decrementando anos.
            
            Returns:
                date: Data resultante do incremento/decremento de anos.
            """

            if self._CalendarType == "FISCAL":
                # Calendário fiscal
                current_fiscal_year, current_fiscal_month = __getFiscalMonthFromDate(self._Date.date())
                target_fiscal_year = current_fiscal_year + self._Increment
                
                if self._Alignment.upper() == "B":
                    # Primeiro dia do ano fiscal (primeira segunda-feira de janeiro)
                    vInterDate = __getFiscalYearStart(target_fiscal_year)
                elif self._Alignment.upper() == "E":
                    # Último dia do ano fiscal (último domingo do 12º mês fiscal)
                    fiscal_year_start = __getFiscalYearStart(target_fiscal_year)
                    _, last_day = __getFiscalMonthInfo(fiscal_year_start, 12, target_fiscal_year)
                    vInterDate = last_day
                else:  # "S" - mesmo dia relativo
                    # Mantém o mesmo mês fiscal e dia relativo
                    fiscal_year_start = __getFiscalYearStart(target_fiscal_year)
                    month_start, month_end = __getFiscalMonthInfo(fiscal_year_start, current_fiscal_month, target_fiscal_year)
                    
                    # Calcula o dia relativo dentro do mês fiscal
                    current_month_start, _ = __getFiscalMonthInfo(__getFiscalYearStart(current_fiscal_year), current_fiscal_month, current_fiscal_year)
                    day_offset = (self._Date.date() - current_month_start).days
                    
                    # Aplica o offset no mês fiscal alvo
                    target_date = month_start + relativedelta(days=day_offset)
                    # Garante que não ultrapassa o fim do mês
                    if target_date > month_end:
                        target_date = month_end
                    vInterDate = target_date
            else:
                # Calendário normal
                vInterYear = self._Date + relativedelta(years=self._Increment)
                
                # Para YEAR, o alinhamento se aplica ao ano, não ao mês
                if self._Alignment.upper() == "B":
                    vInterDate = date(vInterYear.year, 1, 1)  # Primeiro dia do ano
                elif self._Alignment.upper() == "E":
                    vInterDate = date(vInterYear.year, 12, 31)  # Último dia do ano
                else:  # "S" - mesmo dia relativo
                    vGetDate = __getAlignment(
                        vInterYear.year, vInterYear.month, vDayClass)
                    vInterDate = date(vGetDate.year, vGetDate.month, vGetDate.day)

            return vInterDate

        def __getMonth():
            """Calcula a data incrementando/decrementando meses.
            
            Returns:
                date: Data resultante do incremento/decremento de meses.
            """

            if self._CalendarType == "FISCAL":
                # Calendário fiscal
                current_fiscal_year, current_fiscal_month = __getFiscalMonthFromDate(self._Date.date())
                
                # Calcula o mês fiscal alvo
                target_fiscal_month = current_fiscal_month + self._Increment
                target_fiscal_year = current_fiscal_year
                
                # Ajusta ano se necessário
                while target_fiscal_month > 12:
                    target_fiscal_month -= 12
                    target_fiscal_year += 1
                while target_fiscal_month < 1:
                    target_fiscal_month += 12
                    target_fiscal_year -= 1
                
                fiscal_year_start = __getFiscalYearStart(target_fiscal_year)
                month_start, month_end = __getFiscalMonthInfo(fiscal_year_start, target_fiscal_month, target_fiscal_year)
                
                if self._Alignment.upper() == "B":
                    # Primeiro dia do mês fiscal (sempre segunda-feira)
                    vInterDate = month_start
                elif self._Alignment.upper() == "E":
                    # Último dia do mês fiscal (sempre domingo)
                    vInterDate = month_end
                else:  # "S" - mesmo dia relativo
                    # Calcula o dia relativo dentro do mês fiscal atual
                    current_fiscal_year_start = __getFiscalYearStart(current_fiscal_year)
                    current_month_start, current_month_end = __getFiscalMonthInfo(current_fiscal_year_start, current_fiscal_month, current_fiscal_year)
                    day_offset = (self._Date.date() - current_month_start).days
                    
                    # Aplica o offset no mês fiscal alvo
                    target_date = month_start + relativedelta(days=day_offset)
                    # Garante que não ultrapassa o fim do mês
                    if target_date > month_end:
                        target_date = month_end
                    vInterDate = target_date
            else:
                # Calendário normal
                vInterMonth = self._Date + relativedelta(months=self._Increment)
                vGetDate = __getAlignment(
                    vInterMonth.year, vInterMonth.month, vDayClass)
                vInterDate = date(vGetDate.year, vGetDate.month, vGetDate.day)
            
            return vInterDate

        def __getDay(Increment: int):
            """Calcula a data incrementando/decrementando dias.
            
            Args:
                Increment: Número de dias a incrementar/decrementar.
            
            Returns:
                date: Data resultante do incremento/decremento de dias.
            """
            vInterDay = self._Date + relativedelta(days=Increment)

            if self._Alignment.upper() == "S":
                vInterDate = date(vInterDay.year, vInterDay.month, vInterDay.day)
            else:
                vGetDate = __getAlignment(
                    vInterDay.year, vInterDay.month, vInterDay.day)
                vInterDate = date(vGetDate.year, vGetDate.month, vGetDate.day)
            return vInterDate

        def __getBDay(vDate: date, vCountry: str, vState: str):
            """Verifica se uma data é dia útil.
            
            Args:
                vDate: Data a verificar.
                vCountry: Código do país.
                vState: Código do estado/província.
            
            Returns:
                int: 1 se NÃO for dia útil, 0 se for dia útil.
            """
            
            vHoliday = holidays.country_holidays(
                vCountry, subdiv=vState).get(vDate)
            
            weekday = vDate.weekday()  # 0=segunda, 5=sábado, 6=domingo
            
            # Se é feriado, não é dia útil
            if vHoliday is not None:
                return 1
            
            # Verificação de fim de semana
            if self._Weekend is False:
                # Sábado (5) e domingo (6) não são dias úteis
                if weekday >= 5:  # Corrigido: era > 5 (só pegava domingo)
                    return 1
            else:
                # Se Weekend=True, apenas domingo não é dia útil
                if weekday == 6:  # Domingo
                    return 1
            
            return 0

        if self._Interval.upper() == "YEAR":
            vInterDate = __getYear()

        elif self._Interval.upper() == "MONTH":
            vInterDate = __getMonth()

        elif self._Interval.upper() == "DAY":
            vInterDate = __getDay(self._Increment)

        elif self._Interval.upper() == "BDAY":

            checkNegativeIncrement = __checkNegative(self._Increment)
            days_found = 0
            days_needed = abs(self._Increment)
            Increment = 0
            vBusinessDay = None
            max_iterations = 1000  # Proteção contra loop infinito
            iteration = 0

            # Se incremento é 0, retorna a própria data se for dia útil, senão o próximo
            if self._Increment == 0:
                vDate = __getDay(0)
                if __getBDay(vDate, self._Country, self._State) == 0:
                    vInterDate = vDate
                else:
                    # Procura o próximo dia útil
                    Increment = 1
                    while days_found == 0 and iteration < max_iterations:
                        iteration += 1
                        vDate = __getDay(Increment)
                        if __getBDay(vDate, self._Country, self._State) == 0:
                            days_found = 1
                            vBusinessDay = vDate
                        else:
                            Increment += 1
                    if days_found == 0:
                        raise ValueError("Não foi possível encontrar um dia útil. Verifique os parâmetros.")
                    vInterDate = vBusinessDay
            else:
                # Procura N dias úteis
                while days_found < days_needed and iteration < max_iterations:
                    iteration += 1
                    if iteration > max_iterations:
                        raise ValueError(f"Não foi possível encontrar {days_needed} dias úteis. Verifique os parâmetros.")

                    if checkNegativeIncrement is True:
                        Increment -= 1
                    else:
                        Increment += 1

                    vDate = __getDay(Increment)
                    rBday = __getBDay(vDate, self._Country, self._State)  # Corrigido: era self._Contry

                    if rBday == 0:  # É um dia útil
                        days_found += 1
                        vBusinessDay = vDate

                if days_found < days_needed:
                    raise ValueError(f"Não foi possível encontrar {days_needed} dias úteis. Verifique os parâmetros.")

                vInterDate = vBusinessDay
        else:
            raise ValueError(f"Interval '{self._Interval}' não é válido. Use 'YEAR', 'MONTH', 'DAY' ou 'BDAY'.")

        return vInterDate

    def getYearMonth(self) -> int:
        """Retorna o ano e mês no formato YYYYMM.
        
        Returns:
            int: Ano e mês no formato YYYYMM (ex: 202401).
        """

        vData = self.getDates()
        getYearMonth = int(vData.strftime("%Y%m"))

        return int(getYearMonth)
