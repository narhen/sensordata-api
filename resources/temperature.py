import json
from flask_restful import Resource, reqparse
from settings import storage
from errors import InvalidUsage

class Temperature(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, help="user id can not be converted", location="args")
        parser.add_argument("start_time", type=int, required=True, help="Start time can not be converted", location="args")
        parser.add_argument("end_time", type=int, required=True, help="End time can not be converted", location="args")
        args = parser.parse_args()

        if args.start_time > args.end_time:
            raise InvalidUsage("start time can not be bigger than end time")

        temperatures = storage.get_temperatures(args.user_id, args.start_time, args.end_time)
        temperatures = map(lambda x: x.as_dict(), temperatures)

        return { "temperatures": temperatures }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, required=True, help="user id can not be converted")
        parser.add_argument("temperature", type=float, required=True, help="Temperature can not be converted")
        parser.add_argument("time", type=int, required=True, help="Time can not be converted")
        args = dict(parser.parse_args())

        storage.new_temperature(**args)
        return args

