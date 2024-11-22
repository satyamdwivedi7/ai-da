:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_parameters)).
:- use_module(library(csv)).

% Dynamic predicate to store student data
:- dynamic student/3.

% Load data from CSV
load_students_from_csv(File) :-
    csv_read_file(File, Rows, [functor(student)]),
    maplist(assertz, Rows).

% Define rules to check eligibility
eligible_for_scholarship(Student_ID) :-
    student(Student_ID, Attendance_percentage, CGPA),
    Attendance_percentage >= 75,
    CGPA >= 9.0.

permitted_for_exam(Student_ID) :-
    student(Student_ID, Attendance_percentage, _),
    Attendance_percentage >= 75.

% Handle the /scholarship endpoint
:- http_handler('/scholarship', scholarship_handler, []).

% Scholarship eligibility handler with CORS support
scholarship_handler(Request) :-
    http_parameters(Request, [id(IdAtom, [default('')])]),  % Get the 'id' parameter from the request
    atom_number(IdAtom, Id),  % Convert the atom to a number
    format('Access-Control-Allow-Origin: *~n'), % Allow CORS
    format('Content-type: text/plain~n~n'),    % Content-type header
    (   IdAtom \= '' 
    ->  (   eligible_for_scholarship(Id)
        ->  format('Student ~w is eligible for scholarship.~n', [Id])
        ;   format('Student ~w is not eligible for scholarship.~n', [Id])
        )
    ;   format('Missing "id" parameter.~n', [])
    ).

% Start the HTTP server
start_server(Port) :-
    http_server(http_dispatch, [port(Port)]),
    format('Server started at http://localhost:~w~n', [Port]).
