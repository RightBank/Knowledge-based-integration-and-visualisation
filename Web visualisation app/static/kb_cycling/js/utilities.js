function GetScaleDenominator () {
    // {#        get the metre per pixel #}
    var y = map.getSize().y,
        x = map.getSize().x;
    var maxMeters = map.containerPointToLatLng([0, y])
        .distanceTo( map.containerPointToLatLng([x,y]));
    var MeterPerPixel = maxMeters/x ;
    // {#        get the dpi #}

    var ScaleDenpminator = MeterPerPixel * get_dpi()[0] /  0.0254;
    return ScaleDenpminator;
}
function get_dpi (){
    var arrDPI = new Array();
    if (window.screen.deviceXDPI != undefined) {
        arrDPI[0] = window.screen.deviceXDPI;
        arrDPI[1] = window.screen.deviceYDPI;
    }
    else {
        var tmpNode = document.createElement("DIV");
        tmpNode.style.cssText = "width:1in;height:1in;position:absolute;left:0px;top:0px;z-index:99;visibility:hidden";
        document.body.appendChild(tmpNode);
        arrDPI[0] = parseInt(tmpNode.offsetWidth);
        arrDPI[1] = parseInt(tmpNode.offsetHeight);
        tmpNode.parentNode.removeChild(tmpNode);}

    return arrDPI;
}
