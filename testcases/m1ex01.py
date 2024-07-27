m1ex01 = {
	"description": "Return the maximum unsigned value of a byte array",
	"function"   : "uMax",
	"input_type" : ["uint8_t *", "uint8_t"],
	"output_type": "uint8_t",
	"testcase"   : 
	[
		{
			"description": "Positive elements array",
			"input"      : [ [16, 127, 43, 94], 4 ],
		    "output"     : 127,
		    "grade"      : 3, 
		},{
		    "description": "Negative elements array",
			"input"      : [ [-128, -1, -54, -20, -84, -16, -100, -4], 8 ],
		    "output"     : -1,
		    "grade"      : 3, 
		},{
		    "description": "Mixed positive and negative numbers array",
			"input"      : [ [32, -68, 102, 51, -84, 12, 28, -1], 8 ],
		    "output"     : -1,
		    "grade"      : 3, 
		},{
		    "description": "Empty array",
			"input"      : [ [-1], 0 ],
		    "output"     : 0,
		    "grade"      : 1,
		}
	]
}
