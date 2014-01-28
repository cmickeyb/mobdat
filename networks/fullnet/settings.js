{
    "General" :
    {
        "TimeSteps" : 2000,
        "Interval" : 0.100,
        "Connectors" : ["opensim", "sumo", "social", "stats"]
    },

    "NetworkBuilder" :
    {
	"InjectionPrefix" : "IN",
	"ExtensionFiles" : ["networks/fullnet/builder.py"]
    },

    "SocialConnector" :
    {
	"NodeDataFile" : "networks/fullnet/nodedata.js",
        "WaitMean" : 1000.0,
        "WaitSigma" : 200.0,
        "PeopleCount" : 1200
    },

    "OpenSimConnector" :
    {
        "WorldSize" : [810.0, 810.0, 100.0],
        "WorldOffset" : [107.0, 107.0, 26.0],
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
        "NetworkScaleFactor" : 8.0,
        "ConfigFile" : "networks/fullnet/fullnet.sumocfg",
        "ExtensionFiles" : [ ],
        "VelocityFudgeFactor" : 1.0,
        "SumoPort" : 8813
    },

    "RoadTypes" :
    [
	{
	    "Name" : "One Lane Road Segment",
	    "EdgeTypes" : [ "etype1A", "etype1B", "etype1C" ],
	    "ZOffset" : 20.5,
	    "AssetID" : "7c3df98d-4b1e-4d35-92ec-f5bbad5f4596"
	},

	{
	    "Name" : "Two Lane Road Segment",
	    "EdgeTypes" : [ "etype2A", "etype2B", "etype2C" ],
	    "ZOffset" : 20.5,
	    "AssetID" : "ee4f62a8-3311-4808-86f0-b6caa4d62ecc"
	},

	{
	    "Name" : "Parking Lot Segment",
	    "EdgeTypes" : ["parking_entry"],
	    "ZOffset" : 25.25,
	    "AssetID" : "b2b6c88f-e044-493e-a922-7da651138aae"
	},

	{
	    "Name" : "Marble Driveway",
	    "EdgeTypes" : ["driveway"],
	    "ZOffset" : 20.5,
	    "AssetID" : "6d5ad1c2-54db-42a2-8544-b9117d3b1db5"
	},

	{
	    "Name" : "Asphalt Driveway",
	    "EdgeTypes" : ["parking_drive"],
	    "ZOffset" : 25.25,
	    "AssetID" : "5147e8cf-41e5-480c-b9c3-0282bdb3867c"
	}

    ],

    "NodeTypes" :
    [
	{
	    "Name" : "Parking Lot Intersection [* P * P]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Parking Lot Intersection [* P * P]" },
	    "ZOffset" : 20.50,
	    "Padding" : 2.5,
	    "Signature" : ["*", "*", "*", "*"],
            "NodeTypes" : [ "parking_drive_intersection" ]
	},

	{
	    "Name" : "ParkingLot Entry [2L P 2L P]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "ParkingLot Entry [2L P 2L P]" },
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["1L", "P", "1L", "P"],
            "NodeTypes" : [ "priority" ]
	},

	{
	    "Name" : "ParkingLot Entry [2L P 2L 0L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "ParkingLot Entry [2L P 2L 0L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["1L", "P", "1L", "0L"],
            "NodeTypes" : [ "priority" ]
	},

	{
	    "Name" : "Intersection [0L, 0L, 1L, 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [0L, 0L, 1L, 2L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["0L", "0L", "1L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [0L, 0L, 2L, 1L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [0L, 0L, 2L, 1L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["0L", "0L", "2L", "1L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [0L 1L 1L 1L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [0L 1L 1L 1L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["0L", "1L", "1L", "1L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [2L 0L 2L 1L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [2L 0L 2L 1L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["0L", "2L", "1L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [2L 0L 2L 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [2L 0L 2L 2L]"},
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["0L", "2L", "2L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [1L, 2L, 1L, 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [1L, 2L, 1L, 2L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["1L", "2L", "1L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [1L, 2L, 2L, 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [1L, 2L, 2L, 2L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["1L", "2L", "2L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [2L 2L 2L 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [2L 2L 2L 2L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["2L", "2L", "2L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [1L 1L 1L 1L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [1L 1L 1L 1L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["1L", "1L", "1L", "1L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},
	    
	{
	    "Name" : "Intersection [1L 0L 1L 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [1L 0L 1L 2L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["1L", "0L", "1L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},
	
	{
	    "Name" : "Intersection [1L 1L 1L 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [1L 1L 1L 2L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["1L", "1L", "1L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [0L 0L 1L 1L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [0L 0L 1L 1L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["0L", "0L", "1L", "1L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Intersection [0L 0L 2L 2L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection [0L 0L 2L 2L]" },
	    "ZOffset" : 20.5,
	    "Padding" : 7.5,
	    "Signature" : ["0L", "0L", "2L", "2L"],
            "NodeTypes" : [ "stoplight", "priority" ]
	},

	{
	    "Name" : "Residential Row 1way 1lane",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Residential Row 1way 1lane" },
	    "ZOffset" : 25.0,
	    "Padding" : 0,
	    "Signature" : ["0L", "0L", "D", "0L"],
            "NodeTypes" : [ "residence" ]
	},

	{
	    "Name" : "Residential 1way 1lane",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Residential 1way 1lane" },
	    "ZOffset" : 25.4,
	    "Padding" : 0,
	    "Signature" : ["0L", "0L", "D", "0L"],
            "NodeTypes" : [ ],
            "xNodeTypes" : [ "residence" ]
	},

        {
            "Name" : "Business Box [D 0L 0L 0L]",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Business Box [D 0L 0L 0L]" },
            "ZOffset" : 26.0,
            "Padding" : 0,
            "Signature" : ["D", "0L", "0L", "0L"],
            "NodeTypes" : ["business"]
        },

	{
	    "Name" : "Intersection 2Lane Driveway",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection 2Lane Driveway" },
	    "ZOffset" : 20.5,
	    "Padding" : 2.5,
	    "Signature" : ["1L", "D", "1L", "D"],
            "NodeTypes" : [ "driveway" ]
	},

	{
	    "Name" : "Intersection 2Lane Driveway",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection 2Lane Driveway" },
	    "ZOffset" : 20.5,
	    "Padding" : 2.5,
	    "Signature" : ["1L", "0L", "1L", "D"],
            "NodeTypes" : [ "driveway" ]
	},

	{
	    "Name" : "Intersection 2Lane Driveway",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection 2Lane Driveway" },
	    "ZOffset" : 20.5,
	    "Padding" : 2.5,
	    "Signature" : ["1L", "0L", "1L", "0L"],
            "NodeTypes" : [ "driveway" ]
	},

	{
	    "Name" : "Intersection 2Lane Driveway",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection 2Lane Driveway" },
	    "ZOffset" : 20.5,
	    "Padding" : 2.5,
	    "Signature" : ["1L", "0L", "0L", "1L"],
            "NodeTypes" : [ "driveway" ]
	},

	{
	    "Name" : "Intersection 2Lane Driveway",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection 2Lane Driveway" },
	    "ZOffset" : 20.5,
	    "Padding" : 2.5,
	    "Signature" : ["1L", "1L", "0L", "1L"],
            "NodeTypes" : [ "driveway" ]
	},

	{
	    "Name" : "Intersection 4Lane Driveway",
	    "AssetID" : { "ObjectName" : "SumoAssets Nodes", "ItemName" : "Intersection 4Lane Driveway" },
	    "ZOffset" : 20.5,
	    "Padding" : 5,
	    "Signature" : ["2L", "D", "2L", "D"],
            "NodeTypes" : [ "driveway" ]
	}
    ],

    "VehicleTypes" :
    [
        {
            "Name" : "Police Car",
            "Description" : "A blue car",
            "Rate" : 15,
	    "SourceNodeTypes" : [],
	    "DestinationNodeTypes" : [],
	    "Acceleration" : 0.3,
	    "Deceleration" : 0.3,
	    "Sigma" : 0.5,
	    "Length" : 3,
	    "MinGap" : 2,
	    "MaxSpeed" : 2.0,
            "AssetID" : { "ObjectName" : "SumoAssets Vehicles", "ItemName" : "Police Car" },
            "StartParam" : "{}",
            "Position" : [128.0, 128.0, 30.0],
            "Rotation" : [0.0, 0.0, 0.0, 1.0],
            "Velocity" : [0.0, 0.0, 0.0],
            "StartParameter" : "{}"
        },

        {
            "Name" : "Trolly",
            "Description" : "A blue car",
            "Rate" : 15,
	    "SourceNodeTypes" : [],
	    "DestinationNodeTypes" : [],
	    "Acceleration" : 0.3,
	    "Deceleration" : 0.3,
	    "Sigma" : 0.5,
	    "Length" : 3,
	    "MinGap" : 2,
	    "MaxSpeed" : 2.0,
            "AssetID" : { "ObjectName" : "SumoAssets Vehicles", "ItemName" : "Trolly" },
            "StartParam" : "{}",
            "Position" : [128.0, 128.0, 30.0],
            "Rotation" : [0.0, 0.0, 0.0, 1.0],
            "Velocity" : [0.0, 0.0, 0.0],
            "StartParameter" : "{}"
        },

        {
            "Name" : "BlueCar",
            "Description" : "A blue car",
            "Rate" : 15,
	    "SourceNodeTypes" : ["residence", "business"],
	    "DestinationNodeTypes" : ["residence", "business"],
	    "Acceleration" : 0.3,
	    "Deceleration" : 0.3,
	    "Sigma" : 0.5,
	    "Length" : 3,
	    "MinGap" : 2,
	    "MaxSpeed" : 2.0,
            "AssetID" : "65715f46-7dc1-4b4a-ba64-23b9f972bdc4",
            "StartParam" : "{ 'terminate' : 0, 'color' : '<0.0, 0.0, 1.0>', 'scale' : '<1.0, 3.0, 1.0>' }",
            "Position" : [128.0, 128.0, 30.0],
            "Rotation" : [0.0, 0.0, 0.0, 1.0],
            "Velocity" : [0.0, 0.0, 0.0],
            "StartParameter" : "{}"
        },

        {
            "Name" : "OrangeCar",
            "Description" : "A red car",
            "Rate" : 15,
	    "SourceNodeTypes" : ["residence", "business"],
	    "DestinationNodeTypes" : ["residence", "business"],
	    "Acceleration" : 0.8,
	    "Deceleration" : 0.8,
	    "Sigma" : 0.5,
	    "Length" : 2,
	    "MinGap" : 2,
	    "MaxSpeed" : 4.0,
            "AssetID" : "65715f46-7dc1-4b4a-ba64-23b9f972bdc4",
            "StartParam" : "{ 'terminate' : 0, 'color' : '<1.0, 0.5, 0.0>', 'scale' : '<1.0, 3.0, 1.0>' }",
            "Position" : [128.0, 128.0, 30.0],
            "Rotation" : [0.0, 0.0, 0.0, 1.0],
            "Velocity" : [0.0, 0.0, 0.0],
            "StartParameter" : "{}"
        },
        
        {
            "Name" : "PurpleCar",
            "Description" : "A red car",
            "Rate" : 15,
	    "SourceNodeTypes" : ["residence", "business"],
	    "DestinationNodeTypes" : ["residence", "business"],
	    "Acceleration" : 0.2,
	    "Deceleration" : 0.2,
	    "Sigma" : 0.5,
	    "Length" : 2,
	    "MinGap" : 2,
	    "MaxSpeed" : 1.2,
            "AssetID" : "65715f46-7dc1-4b4a-ba64-23b9f972bdc4",
            "StartParam" : "{ 'terminate' : 0, 'color' : '<1.0, 0.0, 1.0>', 'scale' : '<1.0, 3.0, 1.0>' }",
            "Position" : [128.0, 128.0, 30.0],
            "Rotation" : [0.0, 0.0, 0.0, 1.0],
            "Velocity" : [0.0, 0.0, 0.0],
            "StartParameter" : "{}"
        },
        
        {
            "Name" : "RedCar",
            "Description" : "A red car",
            "Rate" : 15,
	    "SourceNodeTypes" : ["residence", "business"],
	    "DestinationNodeTypes" : ["residence", "business"],
	    "Acceleration" : 0.4,
	    "Deceleration" : 0.4,
	    "Sigma" : 0.5,
	    "Length" : 3,
	    "MinGap" : 2,
	    "MaxSpeed" : 3.0,
            "AssetID" : "65715f46-7dc1-4b4a-ba64-23b9f972bdc4",
            "StartParam" : "{ 'terminate' : 0, 'color' : '<1.0, 0.0, 0.0>', 'scale' : '<1.0, 3.0, 1.0>' }",
            "Position" : [128.0, 128.0, 30.0],
            "Rotation" : [0.0, 0.0, 0.0, 1.0],
            "Velocity" : [0.0, 0.0, 0.0],
            "StartParameter" : "{}"
        },

        {
            "Name" : "Train",
            "Description" : "A one car train",
            "Rate" : 0,
	    "SourceNodeTypes" : ["station"],
	    "DestinationNodeTypes" : ["station"],
	    "Acceleration" : 0.1,
	    "Deceleration" : 0.1,
	    "Sigma" : 0.1,
	    "Length" : 8,
	    "MinGap" : 1,
	    "MaxSpeed" : 3.0,
	    "AssetID" : "d8f32d8f-bd4e-4ed7-ba17-3a1420c332e2",
            "Position" : [128.0, 128.0, 30.0],
            "Rotation" : [0.0, 0.0, 0.0, 1.0],
            "Velocity" : [0.0, 0.0, 0.0],
            "StartParameter" : "{}"
        },

        {
            "Name" : "Van",
            "Description" : "A green van",
            "Rate" : 5,
	    "SourceNodeTypes" : ["residence", "business"],
	    "DestinationNodeTypes" : ["residence", "business"],
	    "Acceleration" : 0.2,
	    "Deceleration" : 0.2,
	    "Sigma" : 0.5,
	    "Length" : 4,
	    "MinGap" : 2,
	    "MaxSpeed" : 1.0,
            "AssetID" : "65715f46-7dc1-4b4a-ba64-23b9f972bdc4",
            "StartParam" : "{ 'terminate' : 0, 'color' : '<0.0, 1.0, 0.0>', 'scale' : '<1.5, 5.0, 1.5>' }",
            "StartParameter" : "{}",
            "Position" : [128.0, 128.0, 30.0],
            "Rotation" : [0.0, 0.0, 0.0, 1.0],
            "Velocity" : [0.0, 0.0, 0.0]
        }
    ]
}
