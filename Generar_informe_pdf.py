from fpdf import FPDF
import sys
import json

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Informe de pruebas del equipo", ln=True, align="C")
        self.ln(5)

    def section_title(self, title):
        self.set_font("Arial", "", 10)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def section_body(self, body):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 6, body)
        self.ln(2)

def generar_informe(data, output_path):
    pdf = PDF()
    pdf.add_page()

    # Sección resumen
    pdf.section_title("Informe Equipo")
    resumen_keys = ["SN", 
                    "node_model", 
                    "node_id", 
                    "serial", 
                    "fw", 
                    "FW_bin", 
                    "EOL_Test",
                    "Calibracion_Check"]
    resumen = "\n".join(f"{k}: {data.get(k, '')}" for k in resumen_keys)
    pdf.section_body(resumen)

    # Sección resultados de test
    #pdf.section_title("Resultados de los test")
    #pdf.section_body()
    for key, value in data.items():
        if key not in resumen_keys:
            pdf.cell(0, 6, f'{key}:         {value}', ln=True)

    pdf.output(output_path)

# Entrada principal
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 generar_informe.py '<json_serializado>'")
        sys.exit(1)

    try:
        nombre_informe = sys.argv[1]
        json_input = sys.argv[2]
        data = json.loads(json_input)
    except Exception as e:
        print(f"Error al leer los datos JSON: {e}")
        sys.exit(1)

    generar_informe(data, nombre_informe)
    print("Informe generado correctamente.")

