from flask import json, Response


def responsify(results):
    return Response(json.dumps({"data": results}), mimetype='application/json')
