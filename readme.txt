How to use?

>First, install dependecies (install via kicad python), change kicad version accordingly.
For extract and merge PDFs
"C:\Program Files\KiCad\9.0\bin\python.exe" -m pip install PyPDF2
For creating PDFs from .csv
"C:\Program Files\KiCad\9.0\bin\python.exe" -m pip install reportlab

>Second, you must provide the project directory, as well as the main project name.
Remember that '\' should be used twice '\\' to python recognize. Or use '/'
project_path : path name variable
project_name : project name variable
kicad_cli_path : kicad cli application path


>That's it. If any error occours, contact me: Bruno Claudino - bruno.claudino@estudante.cear.ufpb.br

