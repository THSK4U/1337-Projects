all: clear run

clear:
	clear

run:
	uv run python src
ex:
	uv run python -m moulinette prepare_exercises

cor:
	uv run python -m moulinette evaluate_student_answers --student_answer_path "data/output/function_calling_results.json"
