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
    var efficiencyColumn = sheet.getRange(2, 24, lastRow - 1, 1);  // Assuming column W is the 24rd column
    efficiencyColumn.setNumberFormat('0.00%');  // Format as percentage (1.5 -> 150%)
  
    // Apply a color scale rule to the Gold Efficiency column (adaptive color scale)
    var rule = SpreadsheetApp.newConditionalFormatRule()
      .setGradientMinpoint('#ff0000')  // Dark red for the lowest value
      .setGradientMidpointWithValue('#ffff00', SpreadsheetApp.InterpolationType.PERCENTILE, 50)  // Yellow in the middle
      .setGradientMaxpoint('#00ff00')  // Dark green for the highest value
      .setRanges([efficiencyColumn])
      .build();
  
    // Clear any previous conditional formatting rules and apply the new one
    var rules = sheet.getConditionalFormatRules();
    rules.push(rule);
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
      sheet.setColumnWidth(i, currentWidth + 10);  // Add 10 pixels of extra width
    }
  
    // Log completion of the formatting
    Logger.log('Sheet formatting completed.');
  }