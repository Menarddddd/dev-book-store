from fastapi import HTTPException, status



class HTTPError:

    @staticmethod
    def bad_request(detail: str = "Bad Request"):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = detail
        )
    
    @staticmethod
    def not_found(detail: str = "Not Found"):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = detail
        )
    
    @staticmethod
    def unauthorized(detail: str = "Unauthorized"):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = detail
        )


def validateFormInput(condition: bool, error_func, error_message=None):
    if not condition:
        if error_message:
            error_func(error_message)  
        else:
            error_func() 


def run_validations(validations: list[tuple[bool, str]]):
    for condition, message in validations:
        validateFormInput(condition, HTTPError.bad_request, message)

