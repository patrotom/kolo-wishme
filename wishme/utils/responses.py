from fastapi import HTTPException, status


class ResponseHandler:
    @staticmethod
    def success(message: str, data: dict = None) -> dict:
        return {"message": message, "data": data}

    @staticmethod
    def get_single_success(name: str, id: int, data: dict):
        message = f"Details for {name} with id {id}"
        return ResponseHandler.success(message, data)

    @staticmethod
    def create_success(name: str, id: int, data: dict) -> dict:
        message = f"{name} with id {id} created successfully"
        return ResponseHandler.success(message, data)

    @staticmethod
    def update_success(name: str, id: int, data: dict) -> dict:
        message = f"{name} with id {id} updated successfully"
        return ResponseHandler.success(message, data)

    @staticmethod
    def delete_success(name: str, id: int, data: dict) -> dict:
        message = f"{name} with id {id} deleted successfully"
        return ResponseHandler.success(message, data)

    @staticmethod
    def not_found_error(name: str = "", id: int = None) -> None:
        message = f"{name} With Id {id} Not Found!"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    @staticmethod
    def invalid_token(name: str = "") -> None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid {name} token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
