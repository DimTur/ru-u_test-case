from fastapi import status


post_user_responses = {
    status.HTTP_201_CREATED: {
        "description": "Registration completed successfully",
        "content": {
            "application/json": {
                "example": {"detail": "Registration completed successfully"}
            }
        },
    },
    status.HTTP_400_BAD_REQUEST: {
        "description": "User with this login already exists!",
        "content": {
            "application/json": {
                "example": {"detail": "User with this login already exists!"}
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal server error",
        "content": {
            "application/json": {
                "example": {"detail": "Internal server error occurred"}
            }
        },
    },
}
