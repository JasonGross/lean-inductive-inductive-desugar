#!/usr/bin/env python
# -*- coding: utf-8 -*-

FORALL = "∀"
SIGMA = "Σ"
LAMBDA = "λ"

class inductive_inductives(object):
    def __init__(self, list_of_inductives):
        self._inductives = tuple(list_of_inductives)
    def __repr__(self):
        return('inductive_inductives(%s)' % repr(self._inductives))
    def __str__(self):
        return(r"""namespace pre
inductive %s
end pre

namespace is_good
inductive %s
end is_good

%s""" % ('\nwith '.join(inductive.to_pre() for inductive in self._inductives),
         '\nwith '.join(inductive.to_is_good("pre") for inductive in self._inductives),
         '\n'.join(inductive.to_helpers("pre", "is_good") for inductive in self._inductives)))

class inductive(object):
    def __init__(self, name, telescope, constructors):
        self._name, self._telescope, self._constructors = name, telescope, tuple(constructors)
    def __repr__(self):
        return('inductive(name=%s, telescope=%s, constructors=%s)' % (self._name, self._telescope, self._constructors))
    def to_pre(self):
        return(r"""%(name)s : %(telescope)s :=
| %(constructors)s""" % {'name':self._name, 'telescope':self._telescope.to_pre(), 'constructors':'\n| '.join(constructor.to_pre() for constructor in self._constructors)})
    def to_is_good(self, pre_name):
        return(r"""%(name)s : %(telescope)s :=
| %(constructors)s""" % {'name':self._name, 'telescope':self._telescope.to_is_good(pre_name), 'constructors':'\n| '.join(constructor.to_is_good(pre_name) for constructor in self._constructors)})
    def to_helpers(self, pre_name, is_good_name):
        return(r"""definition %(name)s : %(telescope)s
  := %(LAMBDA)s %(telescope_binders)s, %(SIGMA)s (%(name)s : %(telescope_return)s), %((thing using name)
| %(constructors)""" % {'name':self._name, 'telescope':self._telescope.to_is_good(pre_name), 'constructors':'\n| '.join(constructor.to_is_good(pre_name) for constructor in self._constructors)})

# take in a list of mutual inductives; each 
