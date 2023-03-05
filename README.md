# tox-backtocks
A refreshed backticks tox plugin 

This is a very early stage release. Use it at your own risks.

Here's the roadmap to 1.0 release and our current status:

- [x] define a `backquote var` in `set_env` with a `backquoted expression`
      (and nothing else) and evaluate it through bash, inside the tox virtual
      environment.
- [x] Make of a `backquote var` usable in commands section.
- [x] Allow another variable to be referenced inside the `backquoted
      expression`
- [x] Strip the trailing newline characters of the `backquoted expression`
- [ ] Allow user configure the evaluation of `backquote expression` to be with
      a shell or not (either fork the command directly, either fork a shell
      and evaluate a possible-complex shell expression)
- [ ] Allow a `backquote var` value to contain regular string parts and a
      `backquote expression`
- [ ] Allow a `backquote var` valueu to container more than one `backquote
      expression`
- [ ] Allow user to configure if we should strip the trailing newline
      characters or not.
- [ ] Allow another variable to reuse the evaluated `backquoted expression`
- [ ] Allow another variable to reuse the evaluated `backquoted expression`
      without reevaluating it :)
- [ ] If evaluating through a shell, automatically add said shell to
      `allowlist_externals` section
