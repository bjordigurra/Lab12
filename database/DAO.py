from database.DB_connect import DBConnect
from model.conessione import Connessione
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct Country
                    from go_retailers
                    order by Country 
                """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(Date) as anno
                    from go_daily_sales gds 
                    order by anno
                """

        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRetailersCountry(country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_retailers gr
                    where Country = %s
                """

        cursor.execute(query, (country, ))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllRetailers():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_retailers gr
                """

        cursor.execute(query)

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getConnessioni(country, year, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.Retailer_code as r1, t2.Retailer_code as r2, count(*) as peso
                from (select gds.Retailer_code , gds.Product_number
                from go_daily_sales gds, go_retailers gr 
                where gds.Retailer_code = gr.Retailer_code and gr.Country = %s and year(gds.Date) = %s
                group by gds.Retailer_code , gds.Product_number) as t1
                left join 
                (select gds.Retailer_code , gds.Product_number
                from go_daily_sales gds, go_retailers gr 
                where gds.Retailer_code = gr.Retailer_code and gr.Country = %s and year(gds.Date) = %s
                group by gds.Retailer_code , gds.Product_number) as t2
                on t1.Product_number = t2.Product_number or t2.Retailer_code is null
                where t1.Retailer_code < t2.Retailer_code
                group by t1.Retailer_code, t2.Retailer_code
                """

        cursor.execute(query, (country, year, country, year))

        for row in cursor:
            result.append(Connessione(idMap[row["r1"]], idMap[row["r2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result

