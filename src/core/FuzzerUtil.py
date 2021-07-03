# MIT License
#
# Copyright (c) [2020 - 2021] The yinyang authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import shutil
import pathlib
import logging

from src.base.Utils import random_string, plain, escape, in_list

from config.Config import crash_list, duplicate_list, ignore_list


def in_crash_list(stdout, stderr):
    return in_list(stdout, stderr, crash_list)


def in_duplicate_list(stdout, stderr):
    return in_list(stdout, stderr, duplicate_list)


def in_ignore_list(stdout, stderr):
    return in_list(stdout, stderr, ignore_list)


def admissible_seed_size(seed, args):
    """
    Checks if seed size is below file_size_limit.
    :returns: True if that is the case and False otherwise.
    """
    seed_size_in_bytes = pathlib.Path(seed).stat().st_size
    if seed_size_in_bytes >= args.file_size_limit:
        return False
    return True


def grep_result(stdout):
    """
    Grep the result from the stdout of a solver.
    """
    result = SolverResult()
    for line in stdout.splitlines():
        if re.search("^unsat$", line, flags=re.MULTILINE):
            result.append(SolverQueryResult.UNSAT)
        elif re.search("^sat$", line, flags=re.MULTILINE):
            result.append(SolverQueryResult.SAT)
        elif re.search("^unknown$", line, flags=re.MULTILINE):
            result.append(SolverQueryResult.UNKNOWN)
    return result


def get_seeds(args, strategy):
    if strategy == "opfuzz":
        seeds = args.PATH_TO_SEEDS
    elif strategy == "yinyang":
        if len(args.PATH_TO_SEEDS) > 2:
            seeds = [
                (a, b)
                for a in args.PATH_TO_SEEDS
                for b in args.PATH_TO_SEEDS
            ]
        elif len(args.PATH_TO_SEEDS) == 2:
            seeds = [
                (args.PATH_TO_SEEDS[0], args.PATH_TO_SEEDS[1])
            ]
        else:
            assert False
    else:
        assert False

    return seeds


def init_oracle(args):
    """
    Initialize the oracle. For SemanticFusion the oracle is either sat or
    unsat. For TypeAwareOpMutation the oracle is unknown
    """
    if args.oracle == "unknown":
        return SolverResult(SolverQueryResult.UNKNOWN)
    elif args.oracle == "sat":
        return SolverResult(SolverQueryResult.SAT)
    elif args.oracle == "unsat":
        return SolverResult(SolverQueryResult.UNSAT)
    assert False


def report(scratchfile, bugtype, cli, stdout, stderr, report_id):
    plain_cli = plain(cli)
    # format: <solver><{crash,wrong,invalid_model}><seed>.<random-str>.smt2
    report = "%s/%s-%s-%s-%s.smt2" % (
        self.args.bugsfolder,
        bugtype,
        plain_cli,
        escape(self.currentseeds),
        report_id,
    )
    try:
        shutil.copy(scratchfile, report)
    except Exception:
        logging.error(
            "Could not copy scratchfile to bugfolder.\
             Disk space seems exhausted."
        )
        exit(ERR_EXHAUSTED_DISK)
    logpath = "%s/%s-%s-%s-%s.output" % (
        self.args.bugsfolder,
        bugtype,
        plain_cli,
        escape(self.currentseeds),
        report_id,
    )
    with open(logpath, "w") as log:
        log.write("command: " + cli + "\n")
        log.write("stderr:\n")
        log.write(stderr)
        log.write("stdout:\n")
        log.write(stdout)
    return report

    def report_diff(
        scratchfile,
        bugtype,
        ref_cli,
        ref_stdout,
        ref_stderr,
        sol_cli,
        sol_stdout,
        sol_stderr,
        report_id,
    ):
        plain_cli = plain(sol_cli)
        # format: <solver><{crash,wrong,invalid_model}><seed>.<random-str>.smt2
        report = "%s/%s-%s-%s-%s.smt2" % (
            self.args.bugsfolder,
            bugtype,
            plain_cli,
            escape(self.currentseeds),
            report_id,
        )
        try:
            shutil.copy(scratchfile, report)
        except Exception:
            logging.error("Could not copy scratchfile to bugfolder.\
                Disk space seems exhausted.")
            exit(ERR_EXHAUSTED_DISK)

        logpath = "%s/%s-%s-%s-%s.output" % (
            self.args.bugsfolder,
            bugtype,
            plain_cli,
            escape(self.currentseeds),
            report_id,
        )
        with open(logpath, "w") as log:
            log.write("*** REFERENCE \n")
            log.write("command: " + ref_cli + "\n")
            log.write("stderr:\n")
            log.write(ref_stderr)
            log.write("stdout:\n")
            log.write(ref_stdout)
            log.write("\n\n*** INCORRECT \n")
            log.write("command: " + sol_cli + "\n")
            log.write("stderr:\n")
            log.write(sol_stderr)
            log.write("stdout:\n")
            log.write(sol_stdout)
        return report