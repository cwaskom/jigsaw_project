from api.src import create_app

app = create_app()
app.run(debug = False) ### Was true but that would crash it