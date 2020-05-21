import os

page_template_path = "/templates/page-template.html"
sermon_template_path = "/templates/sermon-template.html"


def generate_page(obj):
    page_template = get_file(os.getcwd() + page_template_path)
    sermon_template = get_file(os.getcwd() + sermon_template_path)

    page = page_template.replace("{{SERMONS}}", sermon_template)

    sermon_body = []
    sermon_row = []

    for i in range(9):
        if i % 3 == 0:
            sermon_body.append("<div class=\"row\">%s</div>" % sermon_row)
    print(page)


def get_file(filename):
    if os.path.isfile(filename):
        with open(filename) as f:
            return f.read()


if __name__ == "__main__":
    generate_page({})
