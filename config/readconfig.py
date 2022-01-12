import configparser
import os

from constants import constant as const


Class ConfParser():
    def __init__():
        current_dir = os.path.abspath('.')
        cf = configparser.ConfigParser()
        config_path = current_dir + "/config.ini"
        cf.read(config_path)

        secs = cf.sections()
        options = cf.options("Mysql-Database")
        
        sql_config = {
                    const.DATABASE_HOST: cf.get(const.DATABASE_MYSQL, const.DATABASE_HOST),
                    const.DATABASE_USER: cf.get(const.DATABASE_MYSQL, const.DATABASE_USER),
                    const.DATABASE_PASSWORD: cf.get(const.DATABASE_MYSQL, const.DATABASE_PASSWORD),
                    const.DATABASE_NAME: cf.get(const.DATABASE_MYSQL, const.DATABASE_NAME),
                    const.DATABASE_CHARSET: cf.get(const.DATABASE_MYSQL,const.DATABASE_CHARSET
                }




