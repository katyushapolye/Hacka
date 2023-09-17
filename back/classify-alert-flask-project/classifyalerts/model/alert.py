import datetime as dt

from marshmallow import Schema, fields
from marshmallow import post_load

class Alert(object):
    def __init__(self, timestamp, dest_ip, dest_port, src_ip, src_port, alert_severity, alert_signature, alert_category, alert_suricata_id):
        self.timestamp = timestamp
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        self.src_ip = src_ip
        self.src_port = src_port
        self.alert_severity = alert_severity
        self.alert_signature = alert_signature
        self.alert_category = alert_category
        self.alert_suricata_id = alert_suricata_id


class AlertSchema(Schema):
    timestamp = fields.Str()
    dest_ip = fields.Str()
    dest_port = fields.Str()
    src_ip = fields.Str()
    src_port = fields.Str()
    alert_severity = fields.Str()
    alert_signature = fields.Str()
    alert_category = fields.Str()
    alert_suricata_id = fields.Str()
    @post_load
    def make_alert(self, data, **kwargs):
        return Alert(**data)