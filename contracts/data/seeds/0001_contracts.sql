INSERT INTO contracts (id, kind, version, location)
VALUES ('openapi-v1', 'OPENAPI', '1.0.0', 'contracts/api/openapi-v1.yaml')
ON CONFLICT (id) DO NOTHING;