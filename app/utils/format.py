from fastapi.responses import JSONResponse


def format_response(status_code: int, response) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=response
    )


def format_error_messages(error_msgs):
    fields = []
    for error in error_msgs.errors():
        fields.append({
            error['loc'][1]: error['msg']
        })

    return {'message': 'validation error', 'fields': fields}