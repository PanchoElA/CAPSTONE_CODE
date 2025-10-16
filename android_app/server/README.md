Simple server for QRPoints app - Sistema REP

Requirements:
- Python 3.8+
- pip

Install:

1. Create a virtualenv (recommended):
   python -m venv venv
   venv\Scripts\activate
2. Install dependencies:
   pip install -r requirements.txt

Run:

   python app.py

The server listens on port 5000. 

## Endpoints:

**Original QRPoints:**
- GET /profiles -> returns JSON list of {name, points}
- POST /points -> accepts JSON {profile, points, code, ts} and updates server-side store
- GET /export.csv -> downloads CSV of profiles
- GET /export.xlsx -> downloads an Excel workbook containing two sheets: `Profiles` and `Scans`.

**New REP System:**
- POST /generate_qr -> generates unique QR with format CODELPA: or TERCERO:
- POST /retorno_rep -> processes bucket return with REP data validation
- GET /reporte_rep/<lote> -> REP report by batch (YYYYMM format)
- GET /export_rep_csv/<lote> -> CSV export of REP returns by batch
- POST /demo/generar_datos -> generates sample data for testing

**Web UI:**
- GET / -> main dashboard with profiles, scans, and links to REP tools
- GET /generador -> QR generator interface
- GET /reportes -> REP reports by batch with statistics

## REP Data Model:

**QR Generated:**
- qr_id (CODELPA:XXX or TERCERO:XXX)
- marca_envase, origen, peso_envase_kg, lote_produccion, tipo_qr

**Returns REP:**
- qr_id, marca_envase, origen, fecha_retorno, estado_retorno
- peso_envase_kg, destino (REUSO_CODELPA / VALORIZACION_INPROPLAS)
- tienda_retorno, evidencia, lote_reporte, cliente_profile, puntos_otorgados

**Business Logic:**
- CODELPA buckets in good/repairable condition → REUSO_CODELPA (150 points)
- All others → VALORIZACION_INPROPLAS (100 points)
- Monthly batches (lote_reporte) for regulatory reporting

To connect the Android app to this server whilst running on your PC, set the `SERVER_BASE` constant in `app/src/main/java/com/example/qrpoints/PointsManager.kt` to your PC's LAN IP and port, for example `http://192.168.1.20:5000`.

Quick test via curl (from another machine on the same LAN):

curl -X POST -H "Content-Type: application/json" -d '{"profile":"Juan","points":100,"code":"abc123","ts": 1695420000000}' http://<PC_IP>:5000/points

Then GET /profiles to verify:

curl http://<PC_IP>:5000/profiles

Download XLSX:

curl -o export.xlsx http://<PC_IP>:5000/export.xlsx

Generate sample QR:

curl -X POST -H "Content-Type: application/json" -d '{"tipo_qr":"CODELPA","marca_envase":"CODELPA","peso_envase_kg":0.5}' http://<PC_IP>:5000/generate_qr

Process return:

curl -X POST -H "Content-Type: application/json" -d '{"qr_id":"CODELPA:ABC123","estado_retorno":"BUENO","cliente_profile":"Juan"}' http://<PC_IP>:5000/retorno_rep

Notes:
- This is a simple test server for local development only. Do not expose it publicly without proper security.
