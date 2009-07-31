<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<!--
 * This file is part of Madas.
 *
 * Madas is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Madas is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Madas.  If not, see <http://www.gnu.org/licenses/>.
 *
 -->
    <title>Metabolomics Australia User and Quote Management System</title>

<link rel="shortcut icon" href="/favicon.ico" />
<link rel="stylesheet" type="text/css" href="static/css/main.css"></link>
<link rel="stylesheet" type="text/css" href="static/js/ext/resources/css/ext-all.css"></link>
<!-- Ext scripts -->
<script type="text/javascript" src="static/js/ext/adapter/ext/ext-base.js"></script>
<script type="text/javascript" src="static/js/ext/ext-all-debug.js"></script>

<!-- Madas scripts -->
<script type="text/javascript" src="static/js/FileUploadField.js"></script>
<script type="text/javascript" src="static/js/GridSearch.js"></script>
<script type="text/javascript" src="static/js/menu.js"></script>
<script type="text/javascript" src="static/js/login.js"></script>
<script type="text/javascript" src="static/js/controller.js"></script>
<script type="text/javascript" src="static/js/dashboard.js"></script>
<script type="text/javascript" src="static/js/admin.js"></script>
<script type="text/javascript" src="static/js/user.js"></script>
<script type="text/javascript" src="static/js/madasJsonReader.js"></script>
<script type="text/javascript" src="static/js/quote.js"></script>


<script>
var callbackCount = 0;
function callbacker(){
    var username = document.getElementById('username').value;
    
    if (username == "" && callbackCount < 5) {
        //console.log("waiting...");
        callbackCount += 1;
        window.setTimeout("callbacker();", 100);
        return;
    }
    
    Ext.madasInitApplication('${ APP_SECURE_URL }', '${ username }', '${ mainContentFunction }', '${ params }');

}
</script>

</head>
<body onLoad="callbacker();">
<div id="north"><div id="appTitle">Metabolomics Australia User and Quote Management System</div><div id="toolbar"/></div></div>
<div id="south">(c) CCG 2009</div>
<div id="centerDiv"></div>
<form id="hiddenForm"></form>
<div id="loginDiv">
<form id="loginForm" action="login/processLogin" method="POST">
<div class="x-form-item"><label class="x-form-item-label">Email address:</label>
<div class="x-form-element">
<input id="username" name="username">
</div>
<div class="x-form-clear-left">
</div>
<div class="x-form-item"><label class="x-form-item-label">Password:</label>
<div class="x-form-element">
<input id="password" name="password" type="password">
</div>
<div class="x-form-clear-left">
</div>
<input type="submit" value="Login" style="margin-left:200px;">
</form>
</div>

</body>
</html>
