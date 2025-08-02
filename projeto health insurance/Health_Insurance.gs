// PA004 Health Insurance Cross-sell
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Health Insurance Prediction')
    .addItem('Get Prediction', 'PredictAll')
    .addToUi();  
}

// Production Server
const host_production = 'health-insurance-api-0ed02a979ac1.herokuapp.com'

// ----------------------------
// ----- Helper Function ------
// ----------------------------
// API Call
function ApiCall(data, endpoint) {
  const url = 'https://' + host_production + endpoint;
  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(data),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(url, options);
    const code = response.getResponseCode();
    const responseText = response.getContentText();

    Logger.log('Status: ' + code);
    Logger.log('Response: ' + responseText);

    if (code !== 200) {
      return { prediction: 'Erro: ' + code };
    }

    const prediction = JSON.parse(responseText);
    return prediction;
  } catch (error) {
    Logger.log('Erro na chamada da API: ' + error);
    return { prediction: 'Erro na chamada' };
  }
}


// Health Insurance Propensity Score Prediction
function PredictAll() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const headers = sheet.getRange('A1:L1').getValues()[0];
  const lastRow = sheet.getLastRow();
  const data = sheet.getRange('A2:L' + lastRow).getValues();

  const idxScore = headers.indexOf('Propensity_Score');

  if (idxScore === -1) {
    SpreadsheetApp.getUi().alert("A coluna 'Propensity_Score' não foi encontrada na planilha.");
    return;
  }

  for (let i = 0; i < data.length; i++) {
    const row = data[i];
    const json_send = {
      id: row[0],
      Gender: row[1],
      Age: row[2],
      Driving_License: row[3],
      Region_Code: row[4],
      Previously_Insured: row[5],
      Vehicle_Age: row[6],
      Vehicle_Damage: row[7],
      Annual_Premium: row[8],
      Policy_Sales_Channel: row[9],
      Vintage: row[10]
    };

    const response = ApiCall(json_send, '/predict');

    if (response && response[0] && response[0].score !== undefined) {
      sheet.getRange(i + 2, idxScore + 1).setValue(response[0].score);
    } else {
      sheet.getRange(i + 2, idxScore + 1).setValue('Erro');
    }
  }
}

