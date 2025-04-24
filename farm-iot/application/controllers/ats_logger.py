from datetime import datetime, timezone, timedelta
from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086, username='cico', password='2020@GreenFeed')
client.switch_database('ats_data')

VN_TZ = timezone(timedelta(hours=7))  # Múi giờ Việt Nam

def log_ats_data(data):
    points = []
    for gen_key in ['gen1', 'gen2']:
        gen = data.get(gen_key)
        if not gen:
            continue

        # Khởi tạo dictionary fields rỗng
        fields = {}
        ia = float(gen.get("ia", -1))
        ib = float(gen.get("ib", -1))
        ic = float(gen.get("ic", -1))
        freq = float(gen.get("freq1", -1))

        if ia != -1:
            fields["ia"] = ia
        if ib != -1:
            fields["ib"] = ib
        if ic != -1:
            fields["ic"] = ic
        if freq != -1:
            fields["freq"] = freq

        # Nếu có ít nhất một giá trị hợp lệ mới lưu
        if fields:
            point = {
                "measurement": "ats_status",
                "tags": {
                    "generator": gen_key
                },
                "time": datetime.now(VN_TZ).isoformat(),
                "fields": fields
            }
            points.append(point)

    if points:
        client.write_points(points)

