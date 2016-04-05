Module pre.
  Inductive Ctx :=
  | nil
  | cons (Γ : Ctx) (x : Ty)
  with Ty :=
       | Pi (Γ : Ctx) (A : Ty) (B : Ty).
End pre.

Module is_good.
  Inductive Ctx : pre.Ctx -> Type :=
  | nil : Ctx pre.nil
  | cons (Γ : pre.Ctx) (x : pre.Ty) : Ctx Γ -> Ty Γ x -> Ctx (pre.cons Γ x)
  with Ty : pre.Ctx -> pre.Ty -> Type :=
       | Pi (Γ : pre.Ctx) (A : pre.Ty) (B : pre.Ty)
         : Ctx Γ -> Ty Γ A -> Ty (pre.cons Γ A) B -> Ty Γ (pre.Pi Γ A B).
End is_good.

Existing Class is_good.Ctx.
Existing Class is_good.Ty.
Existing Instances is_good.nil is_good.cons is_good.Pi.

Record Ctx := { Γ :> pre.Ctx ; Γgood :> is_good.Ctx Γ }.
Record Ty (Γ : Ctx) := { T :> pre.Ty ; Tgood :> is_good.Ty Γ T }.
Existing Instances Γgood Tgood.
Definition nil : Ctx := {| Γ := pre.nil |}.
Definition cons (Γ : Ctx) (x : Ty Γ) := {| Γ := pre.cons Γ x |}.
Definition Pi {Γ : Ctx} (A : Ty Γ) (B : Ty (cons Γ A)) : Ty Γ.
Proof.
  exists (pre.Pi Γ A B).
  apply is_good.Pi; try exact _.
  apply B.
Defined.

Definition Ctx_elim (P : Ctx -> Type) 
