const express = require('express');
const bodyParser = require('body-parser');
const { PythonShell } = require('python-shell');
const path = require('path');

const app = express();
const port = 3001;

app.use(bodyParser.json());

app.post('/predict', (req, res) => {
    const inputData = req.body;

    const options = {
        mode: 'text',
        pythonPath: 'C:\\Users\\MSK\\Desktop\\Учеба\\Финашка\\4\\FlaskApp\\venv\\Scripts\\python.exe', // Убедитесь, что путь к Python правильный
        pythonOptions: ['-u'],
        scriptPath: path.join('C:\\Users\\MSK\\Desktop\\Учеба\\Финашка\\4\\FlaskApp'),
        args: [
            inputData.opening_name,
            inputData.rated,
            inputData.increment_code,
            inputData.turns,
            inputData.white_rating,
            inputData.black_rating
        ]
    };

        let pyshell = new PythonShell('predict.py', options);

    pyshell.on('message', function (message) {
        console.log('Python script output:', message);
        res.json({ prediction: message });
    });

    pyshell.on('error', function (err) {
        console.error('Error running Python script:', err);
        res.status(500).json({ error: err.message });
    });

    pyshell.end(function (err, code, signal) {
        if (err) {
            console.error('Error ending Python script:', err);
            res.status(500).json({ error: err.message });
        }
        console.log('The exit code was: ' + code);
        console.log('The exit signal was: ' + signal);
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});