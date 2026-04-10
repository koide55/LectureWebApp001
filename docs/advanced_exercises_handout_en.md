# Web Application Vulnerability Lab
## Advanced Exercise Handout

This handout provides advanced exercises to be used in addition to the standard classroom exercises.  
The goal is not only to observe the behavior of the teaching app, but also to read code, modify code, and verify behavior so that you gain a deeper understanding of secure and insecure implementations.

## Goals

- Understand vulnerabilities and defenses at the code level
- Be able to explain the difference between safe and unsafe implementations
- Experience implementation decisions through small feature additions and fixes

## Suggested Workflow

1. Finish the basic exercises first
2. Check the current behavior before making changes
3. Read the relevant code
4. Make a small change
5. Test the updated behavior
6. Summarize what you changed and why

## Difficulty Levels

### Beginner

- Read existing code
- Explain the difference between safe and vulnerable implementations
- Make small fixes

### Intermediate

- Add a small new feature
- Implement while thinking about authentication, authorization, CSRF, and output safety

### Advanced

- Add a new vulnerability scenario
- Design with multiple security perspectives in mind
- Propose improvements in the form of a security review

## Submission Format

Include the following items in your submission.

1. Exercise number
2. Files you changed
3. Short summary of your implementation
4. Testing results
5. What you learned

## Evaluation Criteria

- Whether the vulnerability or defense is understood correctly
- Whether the intention of the code change is clear
- Whether testing was performed
- Whether the explanation is concise and logical

## Moodle Submission Guide

| Exercise | Response type | Required items |
|---|---|---|
| B1-B4 | Essay | Exercise number, target files, answer or comparison result |
| I1-I4 | File upload + essay | Exercise number, modified files, implementation summary, testing results |
| A1-A4 | File upload + essay | Exercise number, modified files, design intent, testing results, defense explanation |

Writing guide for essay answers:

- Beginner: 4-6 short lines with numbered answers
- Intermediate: 6-10 short lines, separating implementation and testing
- Advanced: 8-12 short lines, separating problem, implementation, and defense

## Exercise List

| Level | Exercise | Theme |
|---|---|---|
| Beginner | B1 | Read and explain `role_required` |
| Beginner | B2 | Compare SQL injection defenses |
| Beginner | B3 | Compare XSS defenses |
| Beginner | B4 | Compare command injection defenses |
| Intermediate | I1 | Add a new protected page |
| Intermediate | I2 | Extend the profile update feature |
| Intermediate | I3 | Add an admin-only feature |
| Intermediate | I4 | Add a new search feature |
| Advanced | A1 | Implement and fix IDOR |
| Advanced | A2 | Add a more advanced XSS exercise |
| Advanced | A3 | Design a multi-vulnerability scenario |
| Advanced | A4 | Security review |

## Beginner Exercises

### B1 Read and Explain `role_required`

Goal:

- Understand the basics of authorization checks

Tasks:

- Explain how `role_required` works
- Describe the behavior for unauthenticated users and for users who lack the required permission
- Explain how `/admin` is protected

Target files:

- `app/auth/decorators.py`
- `app/routes.py`

### B2 Compare SQL Injection Defenses

Goal:

- Understand the difference between safe and vulnerable code at the implementation level

Tasks:

- Read the implementation for `/users`
- Explain what makes the vulnerable version dangerous
- Explain what is improved in the safe version

Target files:

- `app/services/user_service.py`

### B3 Compare XSS Defenses

Goal:

- Understand the importance of output escaping

Tasks:

- Read the templates for `/reflect` and `/board`
- Explain what changes when `|safe` is used
- Summarize the difference between reflected XSS and stored XSS

Target files:

- `app/templates/reflect.html`
- `app/templates/board.html`

### B4 Compare Command Injection Defenses

Goal:

- Understand why `shell=True` is dangerous

Tasks:

- Compare `safe_ping()` and `unsafe_ping()`
- Explain which lines are dangerous and which lines are part of the defense

Target files:

- `app/services/command_service.py`

## Intermediate Exercises

### I1 Add a New Protected Page

Goal:

- Implement page protection using authentication and authorization

Tasks:

- Add a new page such as `/teacher` or `/staff`
- Restrict access to a specific role
- Enforce the protection on the server side

### I2 Extend the Profile Update Feature

Goal:

- Understand state-changing requests and CSRF protection

Tasks:

- Add one new field to `/profile`
- Make sure it works when CSRF protection is enabled
- Keep the output safe when displaying the new field

### I3 Add an Admin-Only Feature

Goal:

- Think about how to prevent broken authorization

Tasks:

- Add a new feature under `/admin`
- Confirm that a normal user cannot use it

Examples:

- Post list
- Post deletion
- User list

### I4 Add a New Search Feature

Goal:

- Implement a new feature that handles SQL safely

Tasks:

- Add a new search page
- Write the SQL safely
- If you want, create both safe and vulnerable versions and compare them

## Advanced Exercises

### A1 Implement and Fix IDOR

Goal:

- Understand broken authorization in a more concrete way

Tasks:

- Add a page that improperly allows access to another user's data
- Then fix it with a safe version

Examples:

- `/posts/<id>`
- `/profile/<id>`

### A2 Add a More Advanced XSS Exercise

Goal:

- Understand how risk changes depending on the output context

Tasks:

- Add a display feature with a different output context than the existing XSS exercises
- Explain why it is dangerous and how to defend it

### A3 Design a Multi-Vulnerability Scenario

Goal:

- Think about vulnerabilities as combinations

Tasks:

- Design a scenario involving two or more vulnerabilities
- Explain the attack flow and the defense flow

### A4 Security Review

Goal:

- Practice finding issues by yourself

Tasks:

- Identify at least three vulnerabilities or improvement points in the app
- Describe the relevant code locations and a possible fix

## Notes

- Perform these exercises only in a local or classroom environment
- Even if you intentionally create vulnerable code, do not run it in a public environment
- Do not test these techniques against public servers or other people's systems

## References

- Basic exercises: lecture slides and standard teaching materials
- Detailed version: `docs/advanced_exercises_en.md`
