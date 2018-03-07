const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;

const path = require('path');
const url = require('url');
const isDev = require('electron-is-dev');
const child_process = require('child_process');

let mainWindow;
let pyServer;

function createWindow() {
    pyServer = child_process.spawn('python', [
            '-m',
            'rocketleaguereplayanalysis.server',
        ], {
            cwd: path.join(__dirname, '../../') // Project's root folder
        }
    );

    pyServer.stdout.on('data', (data) => {
        console.log(data.toString());
    });
    pyServer.stderr.on('data', (data) => {
        console.log(data.toString());
    });

    mainWindow = new BrowserWindow();
    mainWindow.loadURL(isDev ? 'http://localhost:3000' : `file://${path.join(__dirname, '../build/index.html')}`);
    mainWindow.on('closed', () => mainWindow = null);
    mainWindow.setMenu(null);
    mainWindow.maximize();

    if (isDev) { // Open dev tools
        mainWindow.webContents.openDevTools();
    }
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('quit', () => {
    if (pyServer) {
        pyServer.kill('SIGINT');
    }
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});