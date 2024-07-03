import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        countries = self._model.getAllCountries()
        years = self._model.getAllYears()

        for c in countries:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))

        for y in years:
            self._view.ddyear.options.append(ft.dropdown.Option(y))


    def handle_graph(self, e):
        self._view.txtOut3.controls.clear()
        if self._view.ddyear.value is None or self._view.ddcountry.value is None:
            self._view.create_alert("Selezionare entrambi i parametri!")
            self._view.update_page()
            return

        self._model.buildGraph(self._view.ddcountry.value, self._view.ddyear.value)

        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}."))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumArchi()}."))

        self._view.btn_volume.disabled = False
        self._view.btn_path.disabled = False
        self._view.txtN.disabled = False

        self._view.update_page()


    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()

        volumi = []
        nodi = self._model.getNodiGrafo()

        for nodo in nodi:
            volumi.append((nodo.Retailer_name, self._model.getVolumeNodo(nodo)))

        volumi.sort(key=lambda x: x[1], reverse=True)

        for v in volumi:
            self._view.txtOut2.controls.append(ft.Text(f"{v[0]} --> {v[1]}"))

        self._view.update_page()


    def handle_path(self, e):
        self._view.txtOut3.controls.clear()

        num = self._view.txtN.value
        try: numInt = int(num)
        except ValueError:
            self._view.create_alert("Inserire un valore valido!")
            self._view.update_page()
            return

        if numInt < 2:
            self._view.create_alert("Inserire un valore maggiore o uguale a 2!")
            self._view.update_page()
            return

        bestPath, bestCost = self._model.bestPath(numInt)
        self._view.txtOut3.controls.append(ft.Text(f"Lunghezza cammino: {len(bestPath)}."))
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {bestCost}."))

        for i in range(0, len(bestPath) - 1):
            self._view.txtOut3.controls.append(
                ft.Text(f"{bestPath[i].Retailer_name} --> {bestPath[i+1].Retailer_name}: {self._model._grafo[bestPath[i]][bestPath[i+1]]["weight"]}"))

        self._view.update_page()


