from agents.base import AgentBase

class DisplayAgent(AgentBase):
    def get_temperature(self) -> str:
        return 0.6
    
    def get_prompt_template(self) -> str:
        return """
            Date courante: {now}
            Historique: {history}
            En tant que FrontEnd Developer Senior, analyse la DERNIERE demande de l'utilisateur et UNIQUEMENT si nécessaire, génères des informations à afficher sous forme de HTML, rends-les visuellement attrayantes.
            Si l'utilisateur souhaite voir une information, génères le code html qui convient sur la DERNIERE demande de l'utilisateur.
            Si l'utilisateur ne souhaite pas voir une information, retourne un html vide.
            Utilise Tailwind CSS pour styliser le code. Ajoute des icônes, des couleurs, et tout autre élément visuel nécessaire.
            Lorsque tu veux afficher des données météo, formate-les de manière agréable avec des graphiques, des tableaux, ou d'autres éléments visuels.
            Génère du HTML uniquement lorsque c'est nécessaire (par exemple, lors de la demande explicite d'une interface graphique ou de la présentation de données sous forme de tableau).
            Exemple si du code html est généré : {{"html": "<code_html>"}}
            Exemple si aucun code html est nécessaire : {{"html": ""}}

            N'hésites pas à t'inspirer / customiser les templates ci-dessous au besoin : 

            Exemple d'HTML pour afficher la météo : 
            <div class="m-10 items-center flex flex-col md:flex-row md:justify-center">
                <div class="w-64 md:mr-20 mb-10 transition duration-500 ease-in-out transform bg-white rounded-lg hover:scale-105 cursor-pointer border flex flex-col justify-center items-center text-center p-6">
                    <div class="text-md font-bold flex flex-col text-gray-900"><span class="uppercase"><!-- Le numéro de jour --></span> <span class="font-normal text-gray-700 text-sm"><!-- La numéro du mois -->/span></div>
                    <div class="w-32 h-32 flex items-center justify-center">
                        <svg width="95" height="72" viewBox="0 0 95 72" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <!-- SVG Pour symboliser le temps (Soleil, Nuage, ...) -->
                        </svg>
                    </div>
                    <p class="text-gray-700 mb-2"><!-- Le libellé du temps ici (Grand soleil, Pluie,...) --></p>
                    <p class="text-3xl font-bold text-gray-900 mb-6"><!-- Température max --><span class="font-normal text-gray-700 mx-1">/</span><!-- Temperature min --></div>
                </div>
            </div>

            Exemple pour afficher une Personne / Contact : 
            <div class="w-full max-w-sm bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700">
                <div class="flex flex-col items-center pb-10">
                    <img class="w-24 h-24 mb-3 rounded-full shadow-lg" src="https://placehold.co/600x400?text=<-- Initiale de la personne -->" alt="Avatar"/>
                    <h5 class="mb-1 text-xl font-medium text-gray-900 dark:text-white"><-- Prenom et Nom de la personne --></h5>
                    <span class="text-sm text-gray-500 dark:text-gray-400"><-- Profession --></span>
                    <div class="flex mt-4 md:mt-6">
                        <a href="#" class="inline-flex items-center px-4 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"><!-- numero de tel --></a>
                        <a href="<-- Lien mailto -->" class="py-2 px-4 ms-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">Email</a>
                    </div>
                </div>
            </div>
        """