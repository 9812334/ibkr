from supabase import create_client, Client

url: str = "https://dbcizmxdlufqncxipqwt.supabase.co"
key: str = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRiY2l6bXhkbHVmcW5jeGlwcXd0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDE4NDkxMTMsImV4cCI6MjAxNzQyNTExM30.ys98bhleekrfDJAbrMMqXGsVh1XMa3Vtl8O62s7D5as"
)
supabase: Client = create_client(url, key)
