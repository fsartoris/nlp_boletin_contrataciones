import logging
import datetime
import transform
import load
import extract

def main():
    try:

        fecha = datetime.date.today().strftime("%Y%m%d")
        extract.parse('https://www.boletinoficial.gob.ar', fecha)
        response = transform.process(fecha)

        if not response is None:
            load.process(response)

    except Exception as e:
        logging.error('Error at %s', exc_info=e)


if __name__ == '__main__':
    main()
