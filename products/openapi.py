SCHEMA = {
    'openapi': '3.0.3',
    'info': {
        'title': 'Mercado Local API',
        'version': '1.0.0',
        'description': 'API para catálogo, cuentas y perfil de clientes de Mercado Local.',
    },
    'servers': [{'url': '/'}],
    'components': {
        'securitySchemes': {'BearerAuth': {'type': 'http', 'scheme': 'bearer', 'bearerFormat': 'JWT'}},
        'schemas': {
            'User': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'readOnly': True},
                    'email': {'type': 'string', 'format': 'email'},
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'phone': {'type': 'string', 'description': 'Teléfono de contacto'},
                    'password': {'type': 'string', 'format': 'password', 'writeOnly': True},
                },
                'required': ['email'],
            },
            'Credentials': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'format': 'email'},
                    'password': {'type': 'string', 'format': 'password'},
                },
                'required': ['email', 'password'],
            },
            'Tokens': {
                'type': 'object',
                'properties': {'refresh': {'type': 'string'}, 'access': {'type': 'string'}},
            },
            'RefreshToken': {
                'type': 'object', 'properties': {'refresh': {'type': 'string'}}, 'required': ['refresh'],
            },
        },
    },
    'paths': {
        '/api/v1/users/': {
            'get': {'summary': 'Listar usuarios', 'security': [{'BearerAuth': []}], 'responses': {'200': {'description': 'Usuarios; nunca incluye contraseñas.'}}},
            'post': {'summary': 'Registrar usuario', 'description': 'El password solo se acepta en la solicitud y nunca se devuelve.', 'requestBody': {'required': True, 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/User'}}}}, 'responses': {'201': {'description': 'Usuario creado sin contraseña.'}}},
        },
        '/api/v1/users/{id}/': {
            'parameters': [{'name': 'id', 'in': 'path', 'required': True, 'schema': {'type': 'integer'}}],
            'get': {'summary': 'Consultar usuario', 'security': [{'BearerAuth': []}], 'responses': {'200': {'description': 'Datos del usuario sin contraseña.'}}},
            'put': {'summary': 'Editar usuario', 'description': 'La contraseña existente se conserva si se omite password.', 'security': [{'BearerAuth': []}], 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/User'}}}}, 'responses': {'200': {'description': 'Usuario actualizado sin contraseña.'}}},
            'patch': {'summary': 'Editar parcialmente usuario', 'description': 'La contraseña existente se conserva si se omite password.', 'security': [{'BearerAuth': []}], 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/User'}}}}, 'responses': {'200': {'description': 'Usuario actualizado sin contraseña.'}}},
            'delete': {'summary': 'Eliminar usuario', 'security': [{'BearerAuth': []}], 'responses': {'204': {'description': 'Usuario eliminado.'}}},
        },
        '/api/v1/me/': {'get': {'summary': 'Consultar mis datos personales', 'security': [{'BearerAuth': []}], 'responses': {'200': {'description': 'Perfil autenticado sin contraseña.'}}}},
        '/api/token/': {'post': {'summary': 'Obtener token JWT', 'requestBody': {'required': True, 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Credentials'}}}}, 'responses': {'200': {'description': 'Tokens de acceso y actualización.'}}}},
        '/api/token/refresh/': {'post': {'summary': 'Renovar token JWT', 'requestBody': {'required': True, 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/RefreshToken'}}}}, 'responses': {'200': {'description': 'Nuevo token de acceso.'}}}},
    },
}
