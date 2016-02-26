# Modules ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import argparse

from weekly_employment_report import app
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Main ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    # Obtener los argumentos suministrados por línea de comandos
    args = build_command_line_interface_parser().parse_args()

    # Asociar a la aplicación el manejador de registros de eventos
    if 'LOGGER_HANDLER' in app.config:
        app.logger.addHandler(app.config['LOGGER_HANDLER'])

    # Levantar el servidor de desarrollo
    app.run(host=args.host, port=args.port)
