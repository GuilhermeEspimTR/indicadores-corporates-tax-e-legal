<h1>Estrutura do Projeto</h1>
    <ol>
        <li>
            <strong>Pasta Shared:</strong> Esta pasta deve conter todos os arquivos e componentes que serão compartilhados entre as diferentes telas do aplicativo. Isso inclui arquivos de cache e componentes globais que são reutilizáveis em várias partes do aplicativo.
        </li>
        <li>
            <strong>Pasta Pages:</strong> Nesta pasta, devem estar todas as páginas individuais dos dashboards do aplicativo. Por exemplo, <code>pages/estimate_hours</code>. Se uma página de dashboard contiver subpáginas, estas devem ser organizadas dentro da mesma estrutura, por exemplo, <code>pages/okrs/home</code>, <code>pages/okrs/tabela_grafico_1</code>.
        </li>
        <li>
            <strong>Pasta Components dentro de Pages:</strong> Localizada dentro de cada subpasta de página de dashboard, esta pasta armazena todos os componentes exclusivos daquela tela específica. Esses componentes são específicos para a página e não são compartilhados globalmente.
        </li>
        <li>
            <strong>Pasta Data Loaders dentro de Pages:</strong> Esta pasta contém todos os loaders de dados, que são responsáveis por carregar, formatar e armazenar em cache os dados específicos daquela página. Todas as operações de formatação de dados devem ser implementadas aqui.
        </li>
    </ol>