#include "crow.h"
#include <string>
#include <Python.h>
#include <fstream>

void run_schedule_getter(std::string);

int main()
{
	crow::SimpleApp app;

	CROW_ROUTE(app, "/")
	([](){
	 	crow::response main(200);
		main.set_static_file_info("src/index.html");
		main.set_header("content-type", "text/html");
		return main;
	});

	CROW_ROUTE(app, "/schedule/<string>")
	([](std::string id){
	 	crow::response schedule(200);
		run_schedule_getter(id);
		schedule.set_static_file_info("calendar.ics");
		schedule.set_header("content-type", "text/calendar");
		schedule.set_header("content-disposition", "attachement; filename=\"work-schedule.ics\"");
		return schedule;
	});

	app.port(18080).run();

	return 0;
}

void run_schedule_getter(std::string id)
{
	Py_Initialize();

	std::ofstream file("id.txt");
	file << id;
	file.close();

	FILE *fd = fopen("main.py", "r");
	PyRun_SimpleFileEx(fd, "main.py", 1);

	Py_Finalize();
}
