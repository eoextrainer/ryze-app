-- Seed roles and demo credentials (plaintext for demo only)
INSERT INTO users (username, password, role) VALUES
  ('admin', 'admin123', 'admin'),
  ('ceo', 'ceo123', 'ceo'),
  ('scout', 'scout123', 'scout'),
  ('agent', 'agent123', 'agent'),
  ('club', 'club123', 'club'),
  ('player', 'player123', 'player')
ON CONFLICT (username) DO NOTHING;
