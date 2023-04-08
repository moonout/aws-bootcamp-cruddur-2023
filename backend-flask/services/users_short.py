from lib.db import query_one


class UsersShort:
    @staticmethod
    def run(handle):
        sql = """
            SELECT 
                users.uuid::text,
                users.handle,
                users.display_name
            FROM public.users
            WHERE users.handle = %(handle)s
        """
        result = query_one(sql, {"handle": handle})
        print(result)
        return result
