
import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):

        self._model.build_graph()
        self._view.txt_result.controls.append(ft.Text(
            f"Numero di vertici: {self._model.get_num_of_nodes()} Numero di archi: {self._model.get_num_of_edges()}"))
        self._view.txt_result.controls.append(ft.Text(
            f"Informazioni sui pesi degli archi - valore minino: {self._model.get_min_weight()} e valore massimo: {self._model.get_max_weight()}"))

        self._view.update_page()

    def handle_countedges(self, e):
        threshold = float(self._view.txt_name.value)
        if threshold < self._model.get_min_weight() or threshold > self._model.get_max_weight():
            self._view.create_alert("Valore di soglia non valida!")
            return
        count_bigger, count_smaller = self._model.count_edges(threshold)

        self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso maggiore della soglia: {count_bigger}"))
        self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso minore della soglia: {count_smaller}"))
        self._view.update_page()

    def handle_search(self, e):
        threshold = float(self._view.txt_name.value)
        self._model.searchPath(threshold)
        #self._view.txt_result3.controls.append(
            #ft.Text(f"Numero archi percorso più lungo: {len(self._model._solBest)}"))
        #self._view.update_page()

        self._view.txt_result3.controls.append(ft.Text(
            f"Peso cammino massimo: {str(self._model.computeWeightPath(self._model.solBest))}"))

        for ii in self._model.solBest:
            self._view.txt_result3.controls.append(ft.Text(
                f"{ii[0]} --> {ii[1]}: {str(ii[2]['weight'])}"))
        self._view.update_page()
