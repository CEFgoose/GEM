
STATICBLOCK = """
meta {
  title: "TITLE";
  description: "";
  watch-modified: true;
  version: "";
  icon: "";

}

/* MODIFIED BUT NOT UPLOADED LAYER STYLE */

node:modified::modified_layer {
    symbol-shape: NOTUPNODESHAPE;
    symbol-size: NOTUPNODESIZE;
    symbol-stroke-color: NOTUPNODECOLOR;
    symbol-stroke-width: 3px;
    symbol-fill-opacity: 0.5;
    z-index: -5;
}

way:modified::modified_layer,
node:modified < way::modified_layer {
    width: 6;
    color: transparent;
    opacity: 0;
    casing-width: NOTUPWAYWIDTH;
    casing-color: NOTUPWAYCOLOR;
    casing-opacity: 0.7;
    z-index: -5;
}

/*SELECTED LAYER STYLE*/
node:selected::selected_layer {
    symbol-shape: circle;
    symbol-size: 22;
    symbol-stroke-color: lime;
    symbol-stroke-width: 3px;
    symbol-fill-opacity: 0.5;
    z-index: -5;
}"""



USERBLOCK="""
/* USER SEARCH SETTINGS */
setting::user_USERNAME {
            type:boolean;
            label:tr("Turn User USERNAME On/Off");
            default:true;
            }
/* USER SEARCH SETUP */


*[osm_user_name() == "USERID"][setting("user_USERNAME")] {
  set .USERNAME;
}



/*USER WAY STYLE*/
way.USERNAME{
  z-index: -10;
  casing-color: USERWAYCOLOR;
  casing-width: USERWAYWIDTH;
  casing-opacity: 0.6;
  /*
  text: eval(concat("Highway type =", " ", tag("highway")));
  text-offset: -20;
  */
}

/*USER NODE STYLE*/
node.USERNAME{
  symbol-size: USERNODESIZE;
  symbol-shape: USERNODESHAPE;
  symbol-stroke-color: USERNODECOLOR;
  symbol-stroke-width: 3px;
  symbol-fill-opacity: 0.5;
  z-index: -5;
}"""


TOGGLEDUSERBLOCK="""
/* USER SEARCH SETTINGS */
setting::user_USERNAME {
            type:boolean;
            label:tr("Turn User USERID On/Off");
            default:true;
            }
/* USER SEARCH SETUP */


*[osm_user_name() == "USERID"][setting("user_USERNAME")] {
  set .USERNAME;
}



/*USER WAY STYLE*/
way.USERNAME{
  z-index: -10;
  casing-color: USERWAYCOLOR;
  casing-width: USERWAYWIDTH;
  casing-opacity: 0.6;

}

/*USER NODE STYLE*/
node.USERNAME{
  symbol-size: USERNODESIZE;
  symbol-shape: USERNODESHAPE;
  symbol-stroke-color: USERNODECOLOR;
  symbol-stroke-width: 3px;
  symbol-fill-opacity: 0.5;
  z-index: -5;
}
"""

TIMESEARCHBLOCK= """
/* USER SEARCH SETTINGS */
setting::user_USERID {
            type:boolean;
            label:tr("Turn User USERNAME On/Off");
            default:true;
            }

*[osm_user_name() == "USERID"][eval(JOSM_search("timestamp:SEARCHTIME"))] {
  casing-width: USERWAYWIDTH;
  casing-color: USERWAYCOLOR;
  symbol-size: USERNODESIZE;
  symbol-shape: USERNODESHAPE;
  symbol-stroke-color: USERNODECOLOR;
  symbol-stroke-width: 3px;
}
"""

TOGGLEDTIMESEARCHBLOCK= """
/* USER SEARCH SETTINGS */
setting::user_USERNAME {
            type:boolean;
            label:tr("Turn User USERID On/Off");
            default:true;
            }

*[osm_user_name() == "USERID"][eval(JOSM_search("timestamp:SEARCHTIME"))] {
  casing-width: USERWAYWIDTH;
  casing-color: USERWAYCOLOR;
  symbol-size: USERNODESIZE;
  symbol-shape: USERNODESHAPE;
  symbol-stroke-color: USERNODECOLOR;
  symbol-stroke-width: 3px;
}
"""

