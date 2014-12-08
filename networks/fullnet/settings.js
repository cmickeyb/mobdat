{
    "General" :
    {
        "TimeSteps" : 0,
        "Interval" : 0.200,
        "SecondsPerStep" : 2.0,
        "StartTimeOfDay" : 3.0,
        "MaximumTravelers" : 0, 
	"WorldInfoFile" : "networks/fullnet/data/worldinfo.js",
        "Connectors" : ["opensim", "sumo", "social", "stats"]
    },

    "Builder" :
    {
	"ExtensionFiles" : ["networks/fullnet/layout.py", "networks/fullnet/business.py", "networks/fullnet/people.py"]
    },

    "SocialConnector" :
    {
        "WaitMean" : 1000.0,
        "WaitSigma" : 200.0,
        "PeopleCount" : 1200
    },

    "OpenSimConnector" :
    {
        "WorldSize" : [810.0, 810.0, 100.0],
        "WorldOffset" : [363.0, 363.0, 25.50],
        "WorldCenter" : [768.0, 768.0, 25.50],
        "Scale" : 0.4,
        "PositionDelta" : 0.1,
        "VelocityDelta" : 0.1,
        "AccelerationDelta" : 0.05,
        "EndPoint" : "http://127.0.0.1:7060/Dispatcher/",
        "Scene" : "Fullnet",
        "UpdateThreadCount" : 6,
        "Binary" : true
    },
    
    "SumoConnector" :
    {
	"SumoNetworkPath" : "networks/fullnet/net/",
	"SumoDataFilePrefix" : "network",
        "NetworkScaleFactor" : 10.0,
        "VehicleScaleFactor" : 4.0,
        "ConfigFile" : "networks/fullnet/fullnet.sumocfg",
        "ExtensionFiles" : [ ],
        "VelocityFudgeFactor" : 1.0,
        "SumoPort" : 8813
    },

    "StatsConnector" :
    {
        "CollectObjectDynamics" : true,
        "CollectObjectPattern" : "worker[357]+_trip.*"
    },

    "RoadTypes" :
    [
	{
	    "Name" : "Universal Road Segment",
	    "RoadTypes" : [ "etype1A", "etype1B", "etype1C",
                            "etype2A", "etype2B", "etype2C",
                            "etype3A", "etype3B", "etype3C",
                            "parking_entry", "driveway_road", "parking_drive",
                            "1way2lane", "1way3lane" ],
	    "ZOffset" : 20.5,
	    "AssetID" : { "ObjectName" : "SumoAssets Edges", "ItemName" : "Universal Road Segment" }
	}

    ],

    "IntersectionTypes" :
    [
	{
	    "Name" : "Universal Intersection [* * * *]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Universal Intersection [* * * *]" },
	    "ZOffset" : 20.50,
	    "Padding" : 0.0,
	    "Signature" : ["*/*", "*/*", "*/*", "*/*"],
            "IntersectionTypes" : [ "driveway_node", "parking_drive_intersection", "apartment", "business", "townhouse", "stoplight", "priority" ]
	}
    ],

    "VehicleTypes" : [
        {
            "AssetID" : {
                "ObjectName" : "Model A",
                "ItemName" : "Model A - BLACK"
            },
            "Description" : "Model A - BLACK",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "MinGap" : 2,
            "MaxSpeed" : 0,
            "Sigma" : 0.8,
            "Length" : 2.85,
            "Rate" : 15,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model A - BLACK"
        },
        {
            "MaxSpeed" : 0,
            "Sigma" : 0.8,
            "MinGap" : 2,
            "Rate" : 15,
            "Length" : 2.85,
            "ProfileTypes" : 1,
            "Name" : "Model A - BLUE",
            "Acceleration" : 0,
            "AssetID" : {
                "ObjectName" : "Model A",
                "ItemName" : "Model A - BLUE"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model A - BLUE"
        },
        {
            "Length" : 2.85,
            "Rate" : 15,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model A - GRAY",
            "MaxSpeed" : 0,
            "Sigma" : 0.8,
            "MinGap" : 2,
            "AssetID" : {
                "ItemName" : "Model A - GRAY",
                "ObjectName" : "Model A"
            },
            "Description" : "Model A - GRAY",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0
        },
        {
            "AssetID" : {
                "ItemName" : "Model A - GREEN",
                "ObjectName" : "Model A"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model A - GREEN",
            "Sigma" : 0.8,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Rate" : 15,
            "Length" : 2.85,
            "ProfileTypes" : 1,
            "Name" : "Model A - GREEN",
            "Acceleration" : 0
        },
        {
            "Description" : "Model A - ORANGE",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ItemName" : "Model A - ORANGE",
                "ObjectName" : "Model A"
            },
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model A - ORANGE",
            "Length" : 2.85,
            "Rate" : 15,
            "MinGap" : 2,
            "MaxSpeed" : 0,
            "Sigma" : 0.8
        },
        {
            "Description" : "Model A - PURPLE",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "AssetID" : {
                "ItemName" : "Model A - PURPLE",
                "ObjectName" : "Model A"
            },
            "Acceleration" : 0,
            "Name" : "Model A - PURPLE",
            "ProfileTypes" : 1,
            "Length" : 2.85,
            "Rate" : 15,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Sigma" : 0.8
        },
        {
            "Description" : "Model A - RED",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "AssetID" : {
                "ObjectName" : "Model A",
                "ItemName" : "Model A - RED"
            },
            "Sigma" : 0.8,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model A - RED",
            "Length" : 2.85,
            "Rate" : 15
        },
        {
            "MaxSpeed" : 0,
            "Sigma" : 0.8,
            "MinGap" : 2,
            "Length" : 2.85,
            "Rate" : 15,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model A - WHITE",
            "AssetID" : {
                "ObjectName" : "Model A",
                "ItemName" : "Model A - WHITE"
            },
            "Description" : "Model A - WHITE",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0
        },
        {
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model A - YELLOW",
            "AssetID" : {
                "ItemName" : "Model A - YELLOW",
                "ObjectName" : "Model A"
            },
            "MinGap" : 2,
            "MaxSpeed" : 0,
            "Sigma" : 0.8,
            "Name" : "Model A - YELLOW",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "Rate" : 15,
            "Length" : 2.85
        },
        {
            "MaxSpeed" : 0,
            "Sigma" : 2,
            "MinGap" : 2,
            "Length" : 3.65,
            "Rate" : 35,
            "Acceleration" : 0,
            "Name" : "Model B - BLACK",
            "ProfileTypes" : 1,
            "AssetID" : {
                "ItemName" : "Model B - BLACK",
                "ObjectName" : "Model B"
            },
            "Description" : "Model B - BLACK",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0
        },
        {
            "AssetID" : {
                "ItemName" : "Model B - BLUE",
                "ObjectName" : "Model B"
            },
            "Description" : "Model B - BLUE",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Length" : 3.65,
            "Rate" : 35,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model B - BLUE",
            "Sigma" : 2,
            "MaxSpeed" : 0,
            "MinGap" : 2
        },
        {
            "AssetID" : {
                "ObjectName" : "Model B",
                "ItemName" : "Model B - GRAY"
            },
            "Description" : "Model B - GRAY",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Length" : 3.65,
            "Rate" : 35,
            "Acceleration" : 0,
            "Name" : "Model B - GRAY",
            "ProfileTypes" : 1,
            "Sigma" : 2,
            "MaxSpeed" : 0,
            "MinGap" : 2
        },
        {
            "AssetID" : {
                "ObjectName" : "Model B",
                "ItemName" : "Model B - GREEN"
            },
            "Description" : "Model B - GREEN",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Length" : 3.65,
            "Rate" : 35,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model B - GREEN",
            "Sigma" : 2,
            "MaxSpeed" : 0,
            "MinGap" : 2
        },
        {
            "Sigma" : 2,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Length" : 3.65,
            "Rate" : 35,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model B - ORANGE",
            "AssetID" : {
                "ItemName" : "Model B - ORANGE",
                "ObjectName" : "Model B"
            },
            "Description" : "Model B - ORANGE",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }"
        },
        {
            "Sigma" : 2,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Acceleration" : 0,
            "Name" : "Model B - PURPLE",
            "ProfileTypes" : 1,
            "Length" : 3.65,
            "Rate" : 35,
            "Description" : "Model B - PURPLE",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ItemName" : "Model B - PURPLE",
                "ObjectName" : "Model B"
            }
        },
        {
            "Rate" : 35,
            "Length" : 3.65,
            "Name" : "Model B - RED",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Sigma" : 2,
            "AssetID" : {
                "ObjectName" : "Model B",
                "ItemName" : "Model B - RED"
            },
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model B - RED"
        },
        {
            "Description" : "Model B - WHITE",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ItemName" : "Model B - WHITE",
                "ObjectName" : "Model B"
            },
            "MaxSpeed" : 0,
            "Sigma" : 2,
            "MinGap" : 2,
            "Acceleration" : 0,
            "Name" : "Model B - WHITE",
            "ProfileTypes" : 1,
            "Length" : 3.65,
            "Rate" : 35
        },
        {
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Sigma" : 2,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model B - YELLOW",
            "Length" : 3.65,
            "Rate" : 35,
            "Description" : "Model B - YELLOW",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "AssetID" : {
                "ObjectName" : "Model B",
                "ItemName" : "Model B - YELLOW"
            }
        },
        {
            "Name" : "Model C - BLACK",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "Rate" : 10,
            "Length" : 4,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Sigma" : 3,
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model C - BLACK",
            "AssetID" : {
                "ItemName" : "Model C - BLACK",
                "ObjectName" : "Model C"
            }
        },
        {
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model C - BLUE",
            "Length" : 4,
            "Rate" : 10,
            "MinGap" : 2,
            "MaxSpeed" : 0,
            "Sigma" : 3,
            "Description" : "Model C - BLUE",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "AssetID" : {
                "ItemName" : "Model C - BLUE",
                "ObjectName" : "Model C"
            }
        },
        {
            "MaxSpeed" : 0,
            "Sigma" : 3,
            "MinGap" : 2,
            "Rate" : 10,
            "Length" : 4,
            "Name" : "Model C - GRAY",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "AssetID" : {
                "ItemName" : "Model C - GRAY",
                "ObjectName" : "Model C"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model C - GRAY"
        },
        {
            "AssetID" : {
                "ItemName" : "Model C - GREEN",
                "ObjectName" : "Model C"
            },
            "Description" : "Model C - GREEN",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Length" : 4,
            "Rate" : 10,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model C - GREEN",
            "MaxSpeed" : 0,
            "Sigma" : 3,
            "MinGap" : 2
        },
        {
            "AssetID" : {
                "ObjectName" : "Model C",
                "ItemName" : "Model C - ORANGE"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model C - ORANGE",
            "Sigma" : 3,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Rate" : 10,
            "Length" : 4,
            "Name" : "Model C - ORANGE",
            "ProfileTypes" : 1,
            "Acceleration" : 0
        },
        {
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model C - PURPLE",
            "AssetID" : {
                "ObjectName" : "Model C",
                "ItemName" : "Model C - PURPLE"
            },
            "ProfileTypes" : 1,
            "Name" : "Model C - PURPLE",
            "Acceleration" : 0,
            "Rate" : 10,
            "Length" : 4,
            "Sigma" : 3,
            "MaxSpeed" : 0,
            "MinGap" : 2
        },
        {
            "AssetID" : {
                "ObjectName" : "Model C",
                "ItemName" : "Model C - RED"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model C - RED",
            "Rate" : 10,
            "Length" : 4,
            "Name" : "Model C - RED",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "MaxSpeed" : 0,
            "Sigma" : 3,
            "MinGap" : 2
        },
        {
            "AssetID" : {
                "ItemName" : "Model C - WHITE",
                "ObjectName" : "Model C"
            },
            "Description" : "Model C - WHITE",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Sigma" : 3,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Length" : 4,
            "Rate" : 10,
            "Acceleration" : 0,
            "Name" : "Model C - WHITE",
            "ProfileTypes" : 1
        },
        {
            "Length" : 4,
            "Rate" : 10,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model C - YELLOW",
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Sigma" : 3,
            "AssetID" : {
                "ObjectName" : "Model C",
                "ItemName" : "Model C - YELLOW"
            },
            "Description" : "Model C - YELLOW",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }"
        },
        {
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model D - BLACK",
            "AssetID" : {
                "ItemName" : "Model D - BLACK",
                "ObjectName" : "Model D"
            },
            "MinGap" : 2,
            "MaxSpeed" : 0,
            "Sigma" : 1.75,
            "Name" : "Model D - BLACK",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "Rate" : 35,
            "Length" : 3.65
        },
        {
            "MinGap" : 2,
            "MaxSpeed" : 0,
            "Sigma" : 1.75,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model D - BLUE",
            "Length" : 3.65,
            "Rate" : 35,
            "Description" : "Model D - BLUE",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ObjectName" : "Model D",
                "ItemName" : "Model D - BLUE"
            }
        },
        {
            "AssetID" : {
                "ItemName" : "Model D - GRAY",
                "ObjectName" : "Model D"
            },
            "Description" : "Model D - GRAY",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "MaxSpeed" : 0,
            "Sigma" : 1.75,
            "MinGap" : 2,
            "Length" : 3.65,
            "Rate" : 35,
            "Acceleration" : 0,
            "Name" : "Model D - GRAY",
            "ProfileTypes" : 1
        },
        {
            "Sigma" : 1.75,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Name" : "Model D - GREEN",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "Rate" : 35,
            "Length" : 3.65,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model D - GREEN",
            "AssetID" : {
                "ItemName" : "Model D - GREEN",
                "ObjectName" : "Model D"
            }
        },
        {
            "AssetID" : {
                "ItemName" : "Model D - ORANGE",
                "ObjectName" : "Model D"
            },
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model D - ORANGE",
            "Rate" : 35,
            "Length" : 3.65,
            "ProfileTypes" : 1,
            "Name" : "Model D - ORANGE",
            "Acceleration" : 0,
            "MaxSpeed" : 0,
            "Sigma" : 1.75,
            "MinGap" : 2
        },
        {
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Sigma" : 1.75,
            "Name" : "Model D - PURPLE",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "Rate" : 35,
            "Length" : 3.65,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model D - PURPLE",
            "AssetID" : {
                "ObjectName" : "Model D",
                "ItemName" : "Model D - PURPLE"
            }
        },
        {
            "Rate" : 35,
            "Length" : 3.65,
            "Name" : "Model D - RED",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "MaxSpeed" : 0,
            "Sigma" : 1.75,
            "MinGap" : 2,
            "AssetID" : {
                "ItemName" : "Model D - RED",
                "ObjectName" : "Model D"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model D - RED"
        },
        {
            "AssetID" : {
                "ItemName" : "Model D - WHITE",
                "ObjectName" : "Model D"
            },
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model D - WHITE",
            "Rate" : 35,
            "Length" : 3.65,
            "ProfileTypes" : 1,
            "Name" : "Model D - WHITE",
            "Acceleration" : 0,
            "Sigma" : 1.75,
            "MaxSpeed" : 0,
            "MinGap" : 2
        },
        {
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model D - YELLOW",
            "AssetID" : {
                "ItemName" : "Model D - YELLOW",
                "ObjectName" : "Model D"
            },
            "MaxSpeed" : 0,
            "Sigma" : 1.75,
            "MinGap" : 2,
            "ProfileTypes" : 1,
            "Name" : "Model D - YELLOW",
            "Acceleration" : 0,
            "Rate" : 35,
            "Length" : 3.65
        },
        {
            "Description" : "Model E - BLACK",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "AssetID" : {
                "ObjectName" : "Model E",
                "ItemName" : "Model E - BLACK"
            },
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model E - BLACK",
            "Length" : 3.65,
            "Rate" : 15,
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "MinGap" : 1.5
        },
        {
            "AssetID" : {
                "ObjectName" : "Model E",
                "ItemName" : "Model E - BLUE"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model E - BLUE",
            "MaxSpeed" : 0,
            "MinGap" : 1.5,
            "Sigma" : 1.5,
            "Rate" : 15,
            "Length" : 3.65,
            "ProfileTypes" : 1,
            "Name" : "Model E - BLUE",
            "Acceleration" : 0
        },
        {
            "Length" : 3.65,
            "Rate" : 15,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model E - GRAY",
            "MinGap" : 1.5,
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "AssetID" : {
                "ObjectName" : "Model E",
                "ItemName" : "Model E - GRAY"
            },
            "Description" : "Model E - GRAY",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }"
        },
        {
            "AssetID" : {
                "ObjectName" : "Model E",
                "ItemName" : "Model E - GREEN"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model E - GREEN",
            "Rate" : 15,
            "Length" : 3.65,
            "ProfileTypes" : 1,
            "Name" : "Model E - GREEN",
            "Acceleration" : 0,
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 1.5
        },
        {
            "AssetID" : {
                "ObjectName" : "Model E",
                "ItemName" : "Model E - ORANGE"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model E - ORANGE",
            "Rate" : 15,
            "Length" : 3.65,
            "Name" : "Model E - ORANGE",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "MinGap" : 1.5
        },
        {
            "AssetID" : {
                "ObjectName" : "Model E",
                "ItemName" : "Model E - PURPLE"
            },
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model E - PURPLE",
            "Rate" : 15,
            "Length" : 3.65,
            "Name" : "Model E - PURPLE",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "MinGap" : 1.5
        },
        {
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model E - RED",
            "Length" : 3.65,
            "Rate" : 15,
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 1.5,
            "Description" : "Model E - RED",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ObjectName" : "Model E",
                "ItemName" : "Model E - RED"
            }
        },
        {
            "Rate" : 15,
            "Length" : 3.65,
            "Name" : "Model E - WHITE",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "MinGap" : 1.5,
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "AssetID" : {
                "ObjectName" : "Model E",
                "ItemName" : "Model E - WHITE"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model E - WHITE"
        },
        {
            "Description" : "Model E - YELLOW",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ItemName" : "Model E - YELLOW",
                "ObjectName" : "Model E"
            },
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model E - YELLOW",
            "Length" : 3.65,
            "Rate" : 15,
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "MinGap" : 1.5
        },
        {
            "AssetID" : {
                "ObjectName" : "Model F",
                "ItemName" : "Model F - BLACK"
            },
            "Description" : "Model F - BLACK",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Length" : 3.65,
            "Rate" : 15,
            "Acceleration" : 0,
            "Name" : "Model F - BLACK",
            "ProfileTypes" : 1,
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "MinGap" : 1.5
        },
        {
            "Description" : "Model F - BLUE",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "AssetID" : {
                "ObjectName" : "Model F",
                "ItemName" : "Model F - BLUE"
            },
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model F - BLUE",
            "Length" : 3.65,
            "Rate" : 15,
            "MaxSpeed" : 0,
            "MinGap" : 1.5,
            "Sigma" : 1.5
        },
        {
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 1.5,
            "Acceleration" : 0,
            "Name" : "Model F - GRAY",
            "ProfileTypes" : 1,
            "Length" : 3.65,
            "Rate" : 15,
            "Description" : "Model F - GRAY",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ObjectName" : "Model F",
                "ItemName" : "Model F - GRAY"
            }
        },
        {
            "AssetID" : {
                "ObjectName" : "Model F",
                "ItemName" : "Model F - GREEN"
            },
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model F - GREEN",
            "Rate" : 15,
            "Length" : 3.65,
            "Name" : "Model F - GREEN",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "MinGap" : 1.5
        },
        {
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "MinGap" : 1.5,
            "Name" : "Model F - ORANGE",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "Rate" : 15,
            "Length" : 3.65,
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model F - ORANGE",
            "AssetID" : {
                "ItemName" : "Model F - ORANGE",
                "ObjectName" : "Model F"
            }
        },
        {
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 1.5,
            "Rate" : 15,
            "Length" : 3.65,
            "ProfileTypes" : 1,
            "Name" : "Model F - PURPLE",
            "Acceleration" : 0,
            "AssetID" : {
                "ObjectName" : "Model F",
                "ItemName" : "Model F - PURPLE"
            },
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model F - PURPLE"
        },
        {
            "ProfileTypes" : 1,
            "Name" : "Model F - RED",
            "Acceleration" : 0,
            "Rate" : 15,
            "Length" : 3.65,
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 1.5,
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model F - RED",
            "AssetID" : {
                "ObjectName" : "Model F",
                "ItemName" : "Model F - RED"
            }
        },
        {
            "Description" : "Model F - WHITE",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "AssetID" : {
                "ItemName" : "Model F - WHITE",
                "ObjectName" : "Model F"
            },
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 1.5,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model F - WHITE",
            "Length" : 3.65,
            "Rate" : 15
        },
        {
            "AssetID" : {
                "ItemName" : "Model F - YELLOW",
                "ObjectName" : "Model F"
            },
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model F - YELLOW",
            "Rate" : 15,
            "Length" : 3.65,
            "Name" : "Model F - YELLOW",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "MaxSpeed" : 0,
            "MinGap" : 1.5,
            "Sigma" : 1.5
        },
        {
            "AssetID" : {
                "ItemName" : "Model G - BLACK",
                "ObjectName" : "Model G"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model G - BLACK",
            "Rate" : 10,
            "Length" : 4.25,
            "ProfileTypes" : 1,
            "Name" : "Model G - BLACK",
            "Acceleration" : 0,
            "MaxSpeed" : 0,
            "MinGap" : 1.25,
            "Sigma" : 1.25
        },
        {
            "Description" : "Model G - BLUE",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ObjectName" : "Model G",
                "ItemName" : "Model G - BLUE"
            },
            "Acceleration" : 0,
            "Name" : "Model G - BLUE",
            "ProfileTypes" : 1,
            "Length" : 4.25,
            "Rate" : 10,
            "MinGap" : 1.25,
            "MaxSpeed" : 0,
            "Sigma" : 1.25
        },
        {
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model G - GRAY",
            "AssetID" : {
                "ItemName" : "Model G - GRAY",
                "ObjectName" : "Model G"
            },
            "Name" : "Model G - GRAY",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "Rate" : 10,
            "Length" : 4.25,
            "Sigma" : 1.25,
            "MaxSpeed" : 0,
            "MinGap" : 1.25
        },
        {
            "Description" : "Model G - GREEN",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ObjectName" : "Model G",
                "ItemName" : "Model G - GREEN"
            },
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model G - GREEN",
            "Length" : 4.25,
            "Rate" : 10,
            "MinGap" : 1.25,
            "MaxSpeed" : 0,
            "Sigma" : 1.25
        },
        {
            "AssetID" : {
                "ItemName" : "Model G - ORANGE",
                "ObjectName" : "Model G"
            },
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model G - ORANGE",
            "MaxSpeed" : 0,
            "Sigma" : 1.25,
            "MinGap" : 1.25,
            "Rate" : 10,
            "Length" : 4.25,
            "ProfileTypes" : 1,
            "Name" : "Model G - ORANGE",
            "Acceleration" : 0
        },
        {
            "MinGap" : 1.25,
            "MaxSpeed" : 0,
            "Sigma" : 1.25,
            "ProfileTypes" : 1,
            "Name" : "Model G - PURPLE",
            "Acceleration" : 0,
            "Rate" : 10,
            "Length" : 4.25,
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model G - PURPLE",
            "AssetID" : {
                "ItemName" : "Model G - PURPLE",
                "ObjectName" : "Model G"
            }
        },
        {
            "Length" : 4.25,
            "Rate" : 10,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model G - RED",
            "Sigma" : 1.25,
            "MaxSpeed" : 0,
            "MinGap" : 1.25,
            "AssetID" : {
                "ItemName" : "Model G - RED",
                "ObjectName" : "Model G"
            },
            "Description" : "Model G - RED",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0
        },
        {
            "AssetID" : {
                "ItemName" : "Model G - WHITE",
                "ObjectName" : "Model G"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model G - WHITE",
            "Sigma" : 1.25,
            "MaxSpeed" : 0,
            "MinGap" : 1.25,
            "Rate" : 10,
            "Length" : 4.25,
            "Name" : "Model G - WHITE",
            "ProfileTypes" : 1,
            "Acceleration" : 0
        },
        {
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model G - YELLOW",
            "AssetID" : {
                "ObjectName" : "Model G",
                "ItemName" : "Model G - YELLOW"
            },
            "MinGap" : 1.25,
            "MaxSpeed" : 0,
            "Sigma" : 1.25,
            "ProfileTypes" : 1,
            "Name" : "Model G - YELLOW",
            "Acceleration" : 0,
            "Rate" : 10,
            "Length" : 4.25
        },
        {
            "Description" : "Model H - BLACK",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "AssetID" : {
                "ObjectName" : "Model H",
                "ItemName" : "Model H - BLACK"
            },
            "Acceleration" : 0,
            "Name" : "Model H - BLACK",
            "ProfileTypes" : 1,
            "Length" : 4,
            "Rate" : 25,
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 1.5
        },
        {
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "MinGap" : 1.5,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model H - BLUE",
            "Length" : 4,
            "Rate" : 25,
            "Description" : "Model H - BLUE",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ItemName" : "Model H - BLUE",
                "ObjectName" : "Model H"
            }
        },
        {
            "Description" : "Model H - GRAY",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ItemName" : "Model H - GRAY",
                "ObjectName" : "Model H"
            },
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 1.5,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model H - GRAY",
            "Length" : 4,
            "Rate" : 25
        },
        {
            "AssetID" : {
                "ItemName" : "Model H - GREEN",
                "ObjectName" : "Model H"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model H - GREEN",
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 1.5,
            "Rate" : 25,
            "Length" : 4,
            "Name" : "Model H - GREEN",
            "ProfileTypes" : 1,
            "Acceleration" : 0
        },
        {
            "Description" : "Model H - ORANGE",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "AssetID" : {
                "ObjectName" : "Model H",
                "ItemName" : "Model H - ORANGE"
            },
            "Acceleration" : 0,
            "Name" : "Model H - ORANGE",
            "ProfileTypes" : 1,
            "Length" : 4,
            "Rate" : 25,
            "MinGap" : 1.5,
            "MaxSpeed" : 0,
            "Sigma" : 1.5
        },
        {
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model H - PURPLE",
            "AssetID" : {
                "ItemName" : "Model H - PURPLE",
                "ObjectName" : "Model H"
            },
            "Name" : "Model H - PURPLE",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "Rate" : 25,
            "Length" : 4,
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 1.5
        },
        {
            "AssetID" : {
                "ItemName" : "Model H - RED",
                "ObjectName" : "Model H"
            },
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model H - RED",
            "MaxSpeed" : 0,
            "MinGap" : 1.5,
            "Sigma" : 1.5,
            "Rate" : 25,
            "Length" : 4,
            "ProfileTypes" : 1,
            "Name" : "Model H - RED",
            "Acceleration" : 0
        },
        {
            "AssetID" : {
                "ObjectName" : "Model H",
                "ItemName" : "Model H - WHITE"
            },
            "Description" : "Model H - WHITE",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 1.5,
            "Length" : 4,
            "Rate" : 25,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model H - WHITE"
        },
        {
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "MinGap" : 1.5,
            "Length" : 4,
            "Rate" : 25,
            "Acceleration" : 0,
            "Name" : "Model H - YELLOW",
            "ProfileTypes" : 1,
            "AssetID" : {
                "ObjectName" : "Model H",
                "ItemName" : "Model H - YELLOW"
            },
            "Description" : "Model H - YELLOW",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0
        },
        {
            "Acceleration" : 0,
            "Name" : "Model I - BLACK",
            "ProfileTypes" : 1,
            "Length" : 4.35,
            "Rate" : 10,
            "MinGap" : 1.25,
            "MaxSpeed" : 0,
            "Sigma" : 1.25,
            "Description" : "Model I - BLACK",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ObjectName" : "Model I",
                "ItemName" : "Model I - BLACK"
            }
        },
        {
            "MaxSpeed" : 0,
            "Sigma" : 1.25,
            "MinGap" : 1.25,
            "Rate" : 10,
            "Length" : 4.35,
            "ProfileTypes" : 1,
            "Name" : "Model I - BLUE",
            "Acceleration" : 0,
            "AssetID" : {
                "ItemName" : "Model I - BLUE",
                "ObjectName" : "Model I"
            },
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model I - BLUE"
        },
        {
            "Description" : "Model I - GRAY",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ObjectName" : "Model I",
                "ItemName" : "Model I - GRAY"
            },
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model I - GRAY",
            "Length" : 4.35,
            "Rate" : 10,
            "Sigma" : 1.25,
            "MaxSpeed" : 0,
            "MinGap" : 1.25
        },
        {
            "Length" : 4.35,
            "Rate" : 10,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model I - GREEN",
            "MaxSpeed" : 0,
            "MinGap" : 1.25,
            "Sigma" : 1.25,
            "AssetID" : {
                "ObjectName" : "Model I",
                "ItemName" : "Model I - GREEN"
            },
            "Description" : "Model I - GREEN",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }"
        },
        {
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model I - ORANGE",
            "AssetID" : {
                "ObjectName" : "Model I",
                "ItemName" : "Model I - ORANGE"
            },
            "MinGap" : 1.25,
            "MaxSpeed" : 0,
            "Sigma" : 1.25,
            "Name" : "Model I - ORANGE",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "Rate" : 10,
            "Length" : 4.35
        },
        {
            "AssetID" : {
                "ItemName" : "Model I - PURPLE",
                "ObjectName" : "Model I"
            },
            "Description" : "Model I - PURPLE",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Length" : 4.35,
            "Rate" : 10,
            "Acceleration" : 0,
            "Name" : "Model I - PURPLE",
            "ProfileTypes" : 1,
            "MaxSpeed" : 0,
            "MinGap" : 1.25,
            "Sigma" : 1.25
        },
        {
            "AssetID" : {
                "ObjectName" : "Model I",
                "ItemName" : "Model I - RED"
            },
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model I - RED",
            "Rate" : 10,
            "Length" : 4.35,
            "ProfileTypes" : 1,
            "Name" : "Model I - RED",
            "Acceleration" : 0,
            "Sigma" : 1.25,
            "MaxSpeed" : 0,
            "MinGap" : 1.25
        },
        {
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model I - WHITE",
            "AssetID" : {
                "ItemName" : "Model I - WHITE",
                "ObjectName" : "Model I"
            },
            "Name" : "Model I - WHITE",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "Rate" : 10,
            "Length" : 4.35,
            "MaxSpeed" : 0,
            "Sigma" : 1.25,
            "MinGap" : 1.25
        },
        {
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model I - YELLOW",
            "AssetID" : {
                "ObjectName" : "Model I",
                "ItemName" : "Model I - YELLOW"
            },
            "Name" : "Model I - YELLOW",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "Rate" : 10,
            "Length" : 4.35,
            "MinGap" : 1.25,
            "MaxSpeed" : 0,
            "Sigma" : 1.25
        },
        {
            "AssetID" : {
                "ItemName" : "Model J - BLACK",
                "ObjectName" : "Model J"
            },
            "Description" : "Model J - BLACK",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "MaxSpeed" : 0,
            "MinGap" : 1,
            "Sigma" : 1,
            "Length" : 4.35,
            "Rate" : 5,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model J - BLACK"
        },
        {
            "AssetID" : {
                "ItemName" : "Model J - BLUE",
                "ObjectName" : "Model J"
            },
            "Description" : "Model J - BLUE",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Length" : 4.35,
            "Rate" : 5,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model J - BLUE",
            "MaxSpeed" : 0,
            "MinGap" : 1,
            "Sigma" : 1
        },
        {
            "MaxSpeed" : 0,
            "Sigma" : 1,
            "MinGap" : 1,
            "Acceleration" : 0,
            "Name" : "Model J - GRAY",
            "ProfileTypes" : 1,
            "Length" : 4.35,
            "Rate" : 5,
            "Description" : "Model J - GRAY",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "AssetID" : {
                "ObjectName" : "Model J",
                "ItemName" : "Model J - GRAY"
            }
        },
        {
            "Rate" : 5,
            "Length" : 4.35,
            "Name" : "Model J - GREEN",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "MaxSpeed" : 0,
            "Sigma" : 1,
            "MinGap" : 1,
            "AssetID" : {
                "ItemName" : "Model J - GREEN",
                "ObjectName" : "Model J"
            },
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model J - GREEN"
        },
        {
            "MaxSpeed" : 0,
            "Sigma" : 1,
            "MinGap" : 1,
            "Rate" : 5,
            "Length" : 4.35,
            "ProfileTypes" : 1,
            "Name" : "Model J - ORANGE",
            "Acceleration" : 0,
            "AssetID" : {
                "ObjectName" : "Model J",
                "ItemName" : "Model J - ORANGE"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model J - ORANGE"
        },
        {
            "Rate" : 5,
            "Length" : 4.35,
            "Name" : "Model J - PURPLE",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "MaxSpeed" : 0,
            "MinGap" : 1,
            "Sigma" : 1,
            "AssetID" : {
                "ItemName" : "Model J - PURPLE",
                "ObjectName" : "Model J"
            },
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model J - PURPLE"
        },
        {
            "AssetID" : {
                "ItemName" : "Model J - RED",
                "ObjectName" : "Model J"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model J - RED",
            "Rate" : 5,
            "Length" : 4.35,
            "ProfileTypes" : 1,
            "Name" : "Model J - RED",
            "Acceleration" : 0,
            "Sigma" : 1,
            "MaxSpeed" : 0,
            "MinGap" : 1
        },
        {
            "Length" : 4.35,
            "Rate" : 5,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model J - WHITE",
            "Sigma" : 1,
            "MaxSpeed" : 0,
            "MinGap" : 1,
            "AssetID" : {
                "ObjectName" : "Model J",
                "ItemName" : "Model J - WHITE"
            },
            "Description" : "Model J - WHITE",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }"
        },
        {
            "Description" : "Model J - YELLOW",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ObjectName" : "Model J",
                "ItemName" : "Model J - YELLOW"
            },
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model J - YELLOW",
            "Length" : 4.35,
            "Rate" : 5,
            "MaxSpeed" : 0,
            "MinGap" : 1,
            "Sigma" : 1
        },
        {
            "Rate" : 5,
            "Length" : 4,
            "ProfileTypes" : 1,
            "Name" : "Model K - BLACK",
            "Acceleration" : 0,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Sigma" : 1.5,
            "AssetID" : {
                "ObjectName" : "Model K",
                "ItemName" : "Model K - BLACK"
            },
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model K - BLACK"
        },
        {
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "MinGap" : 2,
            "Rate" : 5,
            "Length" : 4,
            "ProfileTypes" : 1,
            "Name" : "Model K - BLUE",
            "Acceleration" : 0,
            "AssetID" : {
                "ItemName" : "Model K - BLUE",
                "ObjectName" : "Model K"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model K - BLUE"
        },
        {
            "Length" : 4,
            "Rate" : 5,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model K - GRAY",
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "AssetID" : {
                "ItemName" : "Model K - GRAY",
                "ObjectName" : "Model K"
            },
            "Description" : "Model K - GRAY",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }"
        },
        {
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Acceleration" : 0,
            "Name" : "Model K - GREEN",
            "ProfileTypes" : 1,
            "Length" : 4,
            "Rate" : 5,
            "Description" : "Model K - GREEN",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "AssetID" : {
                "ItemName" : "Model K - GREEN",
                "ObjectName" : "Model K"
            }
        },
        {
            "Name" : "Model K - ORANGE",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "Rate" : 5,
            "Length" : 4,
            "MinGap" : 2,
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model K - ORANGE",
            "AssetID" : {
                "ItemName" : "Model K - ORANGE",
                "ObjectName" : "Model K"
            }
        },
        {
            "AssetID" : {
                "ItemName" : "Model K - PURPLE",
                "ObjectName" : "Model K"
            },
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model K - PURPLE",
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "MinGap" : 2,
            "Rate" : 5,
            "Length" : 4,
            "ProfileTypes" : 1,
            "Name" : "Model K - PURPLE",
            "Acceleration" : 0
        },
        {
            "AssetID" : {
                "ObjectName" : "Model K",
                "ItemName" : "Model K - RED"
            },
            "Description" : "Model K - RED",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Length" : 4,
            "Rate" : 5,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model K - RED",
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Sigma" : 1.5
        },
        {
            "ProfileTypes" : 1,
            "Name" : "Model K - WHITE",
            "Acceleration" : 0,
            "Rate" : 5,
            "Length" : 4,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Sigma" : 1.5,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model K - WHITE",
            "AssetID" : {
                "ObjectName" : "Model K",
                "ItemName" : "Model K - WHITE"
            }
        },
        {
            "Acceleration" : 0,
            "Name" : "Model K - YELLOW",
            "ProfileTypes" : 1,
            "Length" : 4,
            "Rate" : 5,
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Description" : "Model K - YELLOW",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ItemName" : "Model K - YELLOW",
                "ObjectName" : "Model K"
            }
        },
        {
            "AssetID" : {
                "ItemName" : "Model L - BLACK",
                "ObjectName" : "Model L"
            },
            "Description" : "Model L - BLACK",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Length" : 3.85,
            "Rate" : 15,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model L - BLACK"
        },
        {
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "ProfileTypes" : 1,
            "Name" : "Model L - BLUE",
            "Acceleration" : 0,
            "Rate" : 15,
            "Length" : 3.85,
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model L - BLUE",
            "AssetID" : {
                "ObjectName" : "Model L",
                "ItemName" : "Model L - BLUE"
            }
        },
        {
            "Description" : "Model L - GRAY",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "AssetID" : {
                "ItemName" : "Model L - GRAY",
                "ObjectName" : "Model L"
            },
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "MinGap" : 2,
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model L - GRAY",
            "Length" : 3.85,
            "Rate" : 15
        },
        {
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model L - GREEN",
            "AssetID" : {
                "ObjectName" : "Model L",
                "ItemName" : "Model L - GREEN"
            },
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "MinGap" : 2,
            "Name" : "Model L - GREEN",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "Rate" : 15,
            "Length" : 3.85
        },
        {
            "Acceleration" : 0,
            "ProfileTypes" : 1,
            "Name" : "Model L - ORANGE",
            "Length" : 3.85,
            "Rate" : 15,
            "MinGap" : 2,
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "Description" : "Model L - ORANGE",
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "AssetID" : {
                "ObjectName" : "Model L",
                "ItemName" : "Model L - ORANGE"
            }
        },
        {
            "Name" : "Model L - PURPLE",
            "ProfileTypes" : 1,
            "Acceleration" : 0,
            "Rate" : 15,
            "Length" : 3.85,
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "MinGap" : 2,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model L - PURPLE",
            "AssetID" : {
                "ObjectName" : "Model L",
                "ItemName" : "Model L - PURPLE"
            }
        },
        {
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Deceleration" : 0,
            "Description" : "Model L - RED",
            "AssetID" : {
                "ItemName" : "Model L - RED",
                "ObjectName" : "Model L"
            },
            "ProfileTypes" : 1,
            "Name" : "Model L - RED",
            "Acceleration" : 0,
            "Rate" : 15,
            "Length" : 3.85,
            "MaxSpeed" : 0,
            "MinGap" : 2,
            "Sigma" : 1.5
        },
        {
            "AssetID" : {
                "ItemName" : "Model L - WHITE",
                "ObjectName" : "Model L"
            },
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "Description" : "Model L - WHITE",
            "MaxSpeed" : 0,
            "Sigma" : 1.5,
            "MinGap" : 2,
            "Rate" : 15,
            "Length" : 3.85,
            "Name" : "Model L - WHITE",
            "ProfileTypes" : 1,
            "Acceleration" : 0
        },
        {
            "Description" : "Model L - YELLOW",
            "Deceleration" : 0,
            "StartParameter" : "{ 'terminate' : 0, 'scale' : 0.5 }",
            "AssetID" : {
                "ObjectName" : "Model L",
                "ItemName" : "Model L - YELLOW"
            },
            "Acceleration" : 0,
            "Name" : "Model L - YELLOW",
            "ProfileTypes" : 1,
            "Length" : 3.85,
            "Rate" : 15,
            "Sigma" : 1.5,
            "MaxSpeed" : 0,
            "MinGap" : 2
        }
    ]
}
