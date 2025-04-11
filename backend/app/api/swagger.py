from flask import jsonify, redirect
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_swagger_ui import get_swaggerui_blueprint

def configure_swagger(app):
    """Configure Swagger UI for the Flask app"""
    
    # Create APISpec object
    spec = APISpec(
        title="NotScrum API",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[MarshmallowPlugin()],
    )
    
    # Define schemas for our API objects
    spec.components.schema("Board", {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "description": {"type": "string"},
        }
    })
    
    spec.components.schema("Lane", {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "board_id": {"type": "integer"},
            "position": {"type": "integer"}
        }
    })
    
    spec.components.schema("Card", {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "lane_id": {"type": "integer"},
            "position": {"type": "integer"},
            "color": {"type": "string"}
        }
    })
    
    # Setup Swagger UI blueprint
    SWAGGER_URL = "/api/docs"
    API_URL = "/static/swagger.json"
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "NotScrum API"
        }
    )
    
    # Add route to serve the swagger.json file
    @app.route("/static/swagger.json")
    def swagger_json():
        return jsonify({
            "openapi": "3.0.2",
            "info": {
                "title": "NotScrum API",
                "version": "1.0.0",
                "description": "API for the NotScrum kanban board application"
            },
            "paths": {
                "/api/boards": {
                    "get": {
                        "summary": "Get all boards",
                        "responses": {
                            "200": {
                                "description": "A list of boards",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "array",
                                            "items": {"$ref": "#/components/schemas/Board"}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "post": {
                        "summary": "Create a new board",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Board"}
                                }
                            }
                        },
                        "responses": {
                            "201": {
                                "description": "Board created successfully",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Board"}
                                    }
                                }
                            },
                            "400": {
                                "description": "Invalid request data"
                            }
                        }
                    }
                },
                "/api/boards/{board_id}": {
                    "get": {
                        "summary": "Get a specific board by ID",
                        "parameters": [
                            {
                                "name": "board_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer"
                                },
                                "description": "ID of the board to retrieve"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Board details",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Board"}
                                    }
                                }
                            },
                            "404": {
                                "description": "Board not found"
                            }
                        }
                    },
                    "put": {
                        "summary": "Update a board",
                        "parameters": [
                            {
                                "name": "board_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer"
                                },
                                "description": "ID of the board to update"
                            }
                        ],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Board"}
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Board updated successfully",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Board"}
                                    }
                                }
                            },
                            "404": {
                                "description": "Board not found"
                            }
                        }
                    },
                    "delete": {
                        "summary": "Delete a board",
                        "parameters": [
                            {
                                "name": "board_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer"
                                },
                                "description": "ID of the board to delete"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Board deleted successfully"
                            },
                            "404": {
                                "description": "Board not found"
                            }
                        }
                    }
                },
                "/api/boards/{board_id}/lanes": {
                    "get": {
                        "summary": "Get all lanes for a specific board",
                        "parameters": [
                            {
                                "name": "board_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer"
                                },
                                "description": "ID of the board to retrieve lanes for"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "A list of lanes for the board",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "array",
                                            "items": {"$ref": "#/components/schemas/Lane"}
                                        }
                                    }
                                }
                            },
                            "404": {
                                "description": "Board not found"
                            }
                        }
                    }
                },
                "/api/lanes": {
                    "get": {
                        "summary": "Get all lanes",
                        "responses": {
                            "200": {
                                "description": "A list of lanes",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "array",
                                            "items": {"$ref": "#/components/schemas/Lane"}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "post": {
                        "summary": "Create a new lane",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Lane"}
                                }
                            }
                        },
                        "responses": {
                            "201": {
                                "description": "Lane created successfully",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Lane"}
                                    }
                                }
                            },
                            "400": {
                                "description": "Invalid request data"
                            }
                        }
                    }
                },
                "/api/lanes/{lane_id}": {
                    "get": {
                        "summary": "Get a specific lane by ID",
                        "parameters": [
                            {
                                "name": "lane_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer"
                                },
                                "description": "ID of the lane to retrieve"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Lane details",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Lane"}
                                    }
                                }
                            },
                            "404": {
                                "description": "Lane not found"
                            }
                        }
                    },
                    "put": {
                        "summary": "Update a lane",
                        "parameters": [
                            {
                                "name": "lane_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer"
                                },
                                "description": "ID of the lane to update"
                            }
                        ],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Lane"}
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Lane updated successfully",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Lane"}
                                    }
                                }
                            },
                            "404": {
                                "description": "Lane not found"
                            }
                        }
                    },
                    "delete": {
                        "summary": "Delete a lane",
                        "parameters": [
                            {
                                "name": "lane_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer"
                                },
                                "description": "ID of the lane to delete"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Lane deleted successfully"
                            },
                            "404": {
                                "description": "Lane not found"
                            }
                        }
                    }
                },
                "/api/lanes/{lane_id}/cards": {
                    "get": {
                        "summary": "Get all cards for a specific lane",
                        "parameters": [
                            {
                                "name": "lane_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer"
                                },
                                "description": "ID of the lane to retrieve cards for"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "A list of cards for the lane",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "array",
                                            "items": {"$ref": "#/components/schemas/Card"}
                                        }
                                    }
                                }
                            },
                            "404": {
                                "description": "Lane not found"
                            }
                        }
                    }
                },
                "/api/cards": {
                    "get": {
                        "summary": "Get all cards",
                        "responses": {
                            "200": {
                                "description": "A list of cards",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "array",
                                            "items": {"$ref": "#/components/schemas/Card"}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "post": {
                        "summary": "Create a new card",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Card"}
                                }
                            }
                        },
                        "responses": {
                            "201": {
                                "description": "Card created successfully",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Card"}
                                    }
                                }
                            },
                            "400": {
                                "description": "Invalid request data"
                            }
                        }
                    }
                },
                "/api/cards/{card_id}": {
                    "get": {
                        "summary": "Get a specific card by ID",
                        "parameters": [
                            {
                                "name": "card_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer"
                                },
                                "description": "ID of the card to retrieve"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Card details",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Card"}
                                    }
                                }
                            },
                            "404": {
                                "description": "Card not found"
                            }
                        }
                    },
                    "put": {
                        "summary": "Update a card",
                        "parameters": [
                            {
                                "name": "card_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer"
                                },
                                "description": "ID of the card to update"
                            }
                        ],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Card"}
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Card updated successfully",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Card"}
                                    }
                                }
                            },
                            "404": {
                                "description": "Card not found"
                            }
                        }
                    },
                    "delete": {
                        "summary": "Delete a card",
                        "parameters": [
                            {
                                "name": "card_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer"
                                },
                                "description": "ID of the card to delete"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Card deleted successfully"
                            },
                            "404": {
                                "description": "Card not found"
                            }
                        }
                    }
                }
            },
            "components": {
                "schemas": {
                    "Board": spec.components.schemas["Board"],
                    "Lane": spec.components.schemas["Lane"],
                    "Card": spec.components.schemas["Card"]
                }
            }
        })
    
    # Register Swagger UI blueprint
    app.register_blueprint(swaggerui_blueprint)
    
    # Add root redirect to Swagger UI
    @app.route('/')
    def api_root():
        return redirect('/api/docs')