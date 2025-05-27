from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)  # Debug=treu should only be used in dev mode, not prod.
