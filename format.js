function formatSheet() {
  // Get the active spreadsheet and sheet
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  // Freeze the first row and first column
  sheet.setFrozenRows(1);
  sheet.setFrozenColumns(1);
  
  // Get the range of data
  var range = sheet.getDataRange();
  
  // Center align all data
  range.setHorizontalAlignment('center');
  

  // Format the header row (row 1)
  var headerRange = sheet.getRange(1, 1, 1, sheet.getLastColumn());  // Row 1, all columns
  headerRange.setBackground('#949292');  // Slightly lighter dark gray background
  headerRange.setFontColor('#000000'); // Black font
  headerRange.setFontSize(12);  // Slightly larger font size
  headerRange.setFontWeight('bold');  // Bold the text
  headerRange.setVerticalAlignment('middle');  // Center vertically
  headerRange.setHorizontalAlignment('center');  // Center horizontally
  
  // Set the row height for the header row
  sheet.setRowHeight(1, 25);  // Increase the row height for the header

  // Get the last non-empty row
  var lastRow = sheet.getLastRow();
  
  // Alternating row colors (excluding column W)
  for (var i = 2; i <= lastRow; i++) {
    if (i % 2 == 0) {
      sheet.getRange(i, 1, 1, sheet.getLastColumn() - 1).setBackground('#a4c2f4');  // Light blue for even rows
    } else {
      sheet.getRange(i, 1, 1, sheet.getLastColumn() - 1).setBackground('#ffffff');  // White for odd rows
    }
  }

  // Format column W (Gold Efficiency)
  var efficiencyColumn = sheet.getRange(2, 24, lastRow - 1, 1);  // Assuming column W is the 23rd column
  efficiencyColumn.setNumberFormat('0.00%');  // Format as percentage (1.5 -> 150%)

  // Apply conditional formatting rules to the Gold Efficiency column

var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
var efficiencyColumn = sheet.getRange("X2:X" + lastRow);

// Greater or equal to 150 - Bright Green
var rule1 = SpreadsheetApp.newConditionalFormatRule()
  .whenNumberGreaterThanOrEqualTo(1.50)
  .setBackground('#00ff00')  // Bright Green
  .setRanges([efficiencyColumn])
  .build();

// Less than 150 - Green
var rule2 = SpreadsheetApp.newConditionalFormatRule()
  .whenNumberLessThan(1.50)
  .whenNumberGreaterThanOrEqualTo(1.00)
  .setBackground('#66ff66')  // Green
  .setRanges([efficiencyColumn])
  .build();

// Less than 100 - Light Green
var rule3 = SpreadsheetApp.newConditionalFormatRule()
  .whenNumberLessThan(1.00)
  .whenNumberGreaterThanOrEqualTo(.80)
  .setBackground('#d7f092')  // Light Green
  .setRanges([efficiencyColumn])
  .build();

// Less than 80 - Yellow
var rule4 = SpreadsheetApp.newConditionalFormatRule()
  .whenNumberLessThan(.80)
  .whenNumberGreaterThanOrEqualTo(.60)
  .setBackground('#ffff00')  // Yellow
  .setRanges([efficiencyColumn])
  .build();

// Less than 60 - Orange
var rule5 = SpreadsheetApp.newConditionalFormatRule()
  .whenNumberLessThan(.60)
  .whenNumberGreaterThanOrEqualTo(.50)
  .setBackground('#ff9900')  // Orange
  .setRanges([efficiencyColumn])
  .build();

// Less than 50 - Red
var rule6 = SpreadsheetApp.newConditionalFormatRule()
  .whenNumberLessThan(.50)
  .setBackground('#ed4e4e')  // Red
  .setRanges([efficiencyColumn])
  .build();

// Remove any previous rules and apply the new set
var rules = sheet.getConditionalFormatRules();
rules.push(rule1, rule2, rule3, rule4, rule5, rule6);
sheet.setConditionalFormatRules(rules);


  // Hide rows past the last non-empty row
  for (var i = lastRow + 1; i <= sheet.getMaxRows(); i++) {
    sheet.hideRows(i);  // Hide all rows after the last row with data
  }
  
  // Hide columns past the last non-empty column
  var lastCol = sheet.getLastColumn();
  for (var j = lastCol + 1; j <= sheet.getMaxColumns(); j++) {
    sheet.hideColumns(j);  // Hide all columns after the last column with data
  }

  // Auto resize columns based on content
  sheet.autoResizeColumns(1, sheet.getLastColumn());

  // Add extra space to each column width
  for (var i = 1; i <= sheet.getLastColumn(); i++) {
    var currentWidth = sheet.getColumnWidth(i);
    sheet.setColumnWidth(i, currentWidth + 20);  // Add 10 pixels of extra width
  }

  // Log completion of the formatting
  Logger.log('Sheet formatting completed.');
}