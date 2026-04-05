# Web Application Vulnerability Lab
## Advanced Exercise Collection

This document provides advanced exercises to be used in addition to the basic in-class exercises.  
The goal is not only to observe the behavior of the existing teaching app, but also to read and modify code so that you can better understand secure and insecure implementations.

## How to Use This Document

- Work on these exercises after finishing the basic exercises
- You do not need to complete every exercise
- Choose exercises from the beginner, intermediate, and advanced sections based on your level
- Some tasks require code changes, testing, and a short written explanation

## Basic Submission Policy

- List the files you changed
- Briefly explain what you changed
- Describe which vulnerability or defense the task is related to
- Summarize your testing results

## Recommended Submission Format

1. Exercise number
2. Modified files
3. Implementation summary
4. Testing results
5. What you learned

## Beginner

The beginner section focuses on reading existing code and making small changes.

### Beginner 1 Read and Explain `role_required`

Goal:

- Understand the basics of authorization checks

Task:

- Read the `role_required` logic and explain what happens when the user is not logged in and when the user lacks the required permission
- Explain why `/admin` is protected

Suggested files:

- `app/auth/decorators.py`
- `app/routes.py`

Deliverables:

- A short explanation of the logic
- The relevant code locations

### Beginner 2 Check the SQL Injection Defense

Goal:

- Understand the difference between the safe and vulnerable implementations at the code level

Task:

- Compare the safe and vulnerable implementations for `/users`
- Explain why placeholders or parameterized queries are effective

Suggested files:

- `app/services/user_service.py`

Deliverables:

- A short explanation of the safe / vulnerable difference
- A summary of the dangerous and safe points

### Beginner 3 Check the XSS Defense

Goal:

- Understand the meaning of output escaping

Task:

- Read the templates for `/reflect` and `/board` and identify where auto-escaping is active
- Explain why `|safe` is dangerous

Suggested files:

- `app/templates/reflect.html`
- `app/templates/board.html`

Deliverables:

- A code-level comparison
- A short explanation of the difference between reflected XSS and stored XSS

### Beginner 4 Check the Command Injection Defense

Goal:

- Understand the difference between `shell=True` and passing arguments as a list

Task:

- Compare `safe_ping()` and `unsafe_ping()`
- Identify which lines are dangerous and which lines are part of the defense

Suggested files:

- `app/services/command_service.py`

Deliverables:

- A comparison table
- A short explanation of the dangerous implementation

## Intermediate

The intermediate section focuses on adding small features and improving the safety of existing functionality.

### Intermediate 1 Add a New Protected Page

Goal:

- Implement page protection using authentication and authorization

Task:

- Add a new page such as `/teacher` or `/staff`
- Make it accessible only to logged-in users with a specific role

Requirements:

- The protection must be enforced on the server side
- Add both a route and a template

Deliverables:

- A short explanation of the new page
- An explanation of the decorator or protection you used
- Testing results

### Intermediate 2 Extend the Profile Update Feature

Goal:

- Understand state-changing requests and CSRF protection

Task:

- Add one new field to `/profile`
- Make sure it works correctly when CSRF protection is enabled
- Display the new field safely

Examples:

- Another self-description field
- Department
- Nickname

Deliverables:

- The field you added
- An explanation of the update logic
- A short explanation from the CSRF and output-safety perspectives

### Intermediate 3 Add an Admin-Only Feature

Goal:

- Think about how to prevent broken authorization

Task:

- Add one new feature under `/admin`
- Example ideas include a post list, post deletion, or a user list
- Confirm that normal users cannot use the feature

Requirements:

- The feature must require the admin role
- You must test the behavior as a normal user

Deliverables:

- A description of the feature
- An explanation of the authorization check
- Testing results

### Intermediate 4 Add a New Search Feature

Goal:

- Write your own safe SQL handling logic

Task:

- Add a new search page
- Example ideas include post search or profile search
- Write the SQL safely

Extension:

- You may implement both a safe and a vulnerable version and compare them

Deliverables:

- What the page searches
- How the SQL is written
- An explanation of the safety considerations

## Advanced

The advanced section focuses on adding new vulnerability scenarios and combining multiple security perspectives.

### Advanced 1 Implement and Fix IDOR

Goal:

- Understand broken authorization in a more concrete way

Task:

- Add a page where another user's data can be accessed improperly
- Then create a safe version that fixes the issue

Examples:

- `/posts/<id>`
- `/profile/<id>`

Perspective:

- Prevent access to another user's data based only on a URL value
- Restrict access to the owner or an administrator

Deliverables:

- An explanation of the vulnerable version
- An explanation of the safe version
- A short summary of what should be authorized

### Advanced 2 Add a More Advanced XSS Exercise

Goal:

- Understand how different output contexts create different risks

Task:

- Add another display feature in addition to the existing XSS exercises
- Think about which output context makes the issue dangerous

Examples:

- Output inside an attribute value
- Embedding data inside a JavaScript string

Deliverables:

- The feature you added
- Why it is dangerous
- How it should be defended

### Advanced 3 Design a Multi-Vulnerability Scenario

Goal:

- Think about vulnerabilities as combinations rather than isolated problems

Task:

- Design a scenario involving two or more vulnerabilities
- For example, combine XSS and CSRF, or broken authorization and IDOR
- Explain the attack flow and the defense flow

Deliverables:

- Scenario description
- The related features
- Attack flow
- Defense flow

### Advanced 4 Security Review Exercise

Goal:

- Practice finding vulnerabilities by yourself

Task:

- Review the entire teaching app and identify at least three vulnerabilities or improvement points
- You may include issues already covered in class, but you must point to the relevant code locations
- Propose a fix for each issue

Deliverables:

- A list of issues
- The related code locations
- A proposed fix for each issue

## Suggested Workflow

Recommended approach:

1. Read the existing code first
2. Confirm the behavior before making changes
3. Make a small change
4. Test the behavior again
5. Explain what changed and why

## Evaluation Criteria

- Whether the vulnerability or defense is understood correctly
- Whether the intent of the code change is clear
- Whether testing was performed
- Whether the explanation is logical and clear

## Notes

- Perform these exercises only in a local or classroom environment
- Even when intentionally creating vulnerable code, do not run it in a public environment
- Do not test these techniques on other people's computers or public servers

## Reference

- Refer to the lecture slides and the standard teaching materials for the basic exercises
- In the advanced exercises, aim to explain the difference between the safe and vulnerable versions in your own words
