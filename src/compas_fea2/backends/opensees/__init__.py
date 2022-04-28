"""
********************************************************************************
Opensees
********************************************************************************

reference for OpenSees commands:
https://opensees.github.io/OpenSeesDocumentation/user/userManual.html
"""

from pydoc import ErrorDuringImport
import compas_fea2

from compas.plugins import plugin

# Models
from compas_fea2.model import Model
from compas_fea2.model import Part
from compas_fea2.model import Node
# Elements
from compas_fea2.model.elements import (
    MassElement,
    BeamElement,
    TrussElement,
    MembraneElement,
    ShellElement,
    SolidElement,
)
# Sections
from compas_fea2.model.sections import (
    AngleSection,
    BeamSection,
    BoxSection,
    CircularSection,
    HexSection,
    ISection,
    MassSection,
    PipeSection,
    RectangularSection,
    SpringSection,
    StrutSection,
    TieSection,
    TrapezoidalSection,
    TrussSection,
    MembraneSection,
    ShellSection,
    SolidSection,
)
# Materials
from compas_fea2.model.materials import (
    ElasticIsotropic,
    ElasticOrthotropic,
    ElasticPlastic,
    Stiff,
    UserMaterial,
    Concrete,
    ConcreteDamagedPlasticity,
    ConcreteSmearedCrack,
    Steel,
)
# Groups
from compas_fea2.model.groups import (
    NodesGroup,
    ElementsGroup,
    FacesGroup,
)
# Interactions
from compas_fea2.model.interactions import (
    HardContactFrictionPenalty,
)
# Constraints
from compas_fea2.model.constraints import (
    TieConstraint,
)
# Releases
from compas_fea2.model.releases import (
    BeamEndPinRelease,
)

# Boundary Conditions
from compas_fea2.model.bcs import (
    FixedBC,
    FixedBCXX,
    FixedBCYY,
    FixedBCZZ,
    PinnedBC,
    RollerBCX,
    RollerBCXY,
    RollerBCXZ,
    RollerBCY,
    RollerBCYZ,
    RollerBCZ,
)

# Problem
from compas_fea2.problem import Problem
# Steps
from compas_fea2.problem.steps import (
    ModalAnalysis,
    ComplexEigenValue,
    StaticStep,
    LinearStaticPerturbation,
    BucklingAnalysis,
    DynamicStep,
    QuasiStaticStep,
    DirectCyclicStep,
)
# Loads
from compas_fea2.problem.loads import (
    PointLoad,
    LineLoad,
    AreaLoad,
    TributaryLoad,
    PrestressLoad,
    GravityLoad,
    HarmonicPointLoad,
    HarmonicPressureLoad,
)
# Displacements
from compas_fea2.problem.displacements import (
    GeneralDisplacement,
)
# Outputs
from compas_fea2.problem.outputs import (
    FieldOutput,
    HistoryOutput,
)

# Results
from compas_fea2.results import (
    Results
)

# Input File
from compas_fea2.job import (
    InputFile,
    ParametersFile,
)
# =========================================================================
#                           OPENSEES CLASSES
# =========================================================================

try:
    # Opensees Models
    from .model import OpenseesModel
    from .model import OpenseesPart
    from .model import OpenseesNode

    # Opensees Elements
    from .model.elements import (
        OpenseesMassElement,
        OpenseesBeamElement,
        OpenseesTrussElement,
        OpenseesMembraneElement,
        OpenseesShellElement,
        OpenseesSolidElement,
    )

    # Opensees Sections
    from .model.sections import (
        OpenseesAngleSection,
        OpenseesBeamSection,
        OpenseesBoxSection,
        OpenseesCircularSection,
        OpenseesHexSection,
        OpenseesISection,
        OpenseesMassSection,
        OpenseesPipeSection,
        OpenseesRectangularSection,
        OpenseesSpringSection,
        OpenseesStrutSection,
        OpenseesTieSection,
        OpenseesTrapezoidalSection,
        OpenseesTrussSection,
        OpenseesMembraneSection,
        OpenseesShellSection,
        OpenseesSolidSection,
    )

    # Opensees Materials
    from .model.materials import (
        OpenseesElasticIsotropic,
        OpenseesElasticOrthotropic,
        OpenseesElasticPlastic,
        OpenseesStiff,
        OpenseesUserMaterial,
        OpenseesConcrete,
        OpenseesConcreteDamagedPlasticity,
        OpenseesConcreteSmearedCrack,
        OpenseesSteel,
    )

    # Opensees Groups
    from .model.groups import (
        OpenseesNodesGroup,
        OpenseesElementsGroup,
        OpenseesFacesGroup,
    )

    # Opensees Interactions
    from .model.interactions import (
        OpenseesHardContactFrictionPenalty,
    )
    # Opensees Constraints
    from .model.constraints import (
        OpenseesTieConstraint,
    )

    # Opensees release
    from .model.releases import (
        OpenseesBeamEndPinRelease,
    )

    # Opensees Boundary Conditions
    from .model.bcs import (
        OpenseesFixedBC,
        OpenseesFixedBCXX,
        OpenseesFixedBCYY,
        OpenseesFixedBCZZ,
        OpenseesPinnedBC,
        OpenseesRollerBCX,
        OpenseesRollerBCXY,
        OpenseesRollerBCXZ,
        OpenseesRollerBCY,
        OpenseesRollerBCYZ,
        OpenseesRollerBCZ,
    )

    # Opensees Problem
    from .problem import OpenseesProblem

    # Opensees Steps
    from .problem.steps import (
        OpenseesModalAnalysis,
        OpenseesComplexEigenValue,
        OpenseesStaticStep,
        OpenseesLinearStaticPerturbation,
        OpenseesBucklingAnalysis,
        OpenseesDynamicStep,
        OpenseesQuasiStaticStep,
        OpenseesDirectCyclicStep,
    )
    # Opensees Loads
    from .problem.loads import (
        OpenseesPointLoad,
        OpenseesLineLoad,
        OpenseesAreaLoad,
        OpenseesTributaryLoad,
        OpenseesPrestressLoad,
        OpenseesGravityLoad,
        OpenseesHarmonicPointLoad,
        OpenseesHarmonicPressureLoad,
    )

    # Opensees Displacements
    from .problem.displacements import (
        OpenseesGeneralDisplacement,
    )

    # Opensees outputs
    from .problem.outputs import (
        OpenseesFieldOutput,
        OpenseesHistoryOutput,
    )

    # Opensees Results
    from .results import (
        OpenseesResults
    )

    # Opensees Input File
    from .job import(
        OpenseesInputFile,
        OpenseesParametersFile,
    )

    @plugin(category='fea_backends')
    def register_backend():
        backend = compas_fea2.BACKENDS['opensees']

        backend[Model] = OpenseesModel
        backend[Part] = OpenseesPart
        backend[Node] = OpenseesNode

        backend[MassElement] = OpenseesMassElement
        backend[BeamElement] = OpenseesBeamElement
        backend[TrussElement] = OpenseesTrussElement
        backend[MembraneElement] = OpenseesMembraneElement
        backend[ShellElement] = OpenseesShellElement
        backend[SolidElement] = OpenseesSolidElement

        backend[AngleSection] = OpenseesAngleSection
        backend[BeamSection] = OpenseesBeamSection
        backend[BoxSection] = OpenseesBoxSection
        backend[CircularSection] = OpenseesCircularSection
        backend[HexSection] = OpenseesHexSection
        backend[ISection] = OpenseesISection
        backend[MassSection] = OpenseesMassSection
        backend[MembraneSection] = OpenseesMembraneSection
        backend[PipeSection] = OpenseesPipeSection
        backend[RectangularSection] = OpenseesRectangularSection
        backend[ShellSection] = OpenseesShellSection
        backend[SolidSection] = OpenseesSolidSection
        backend[SpringSection] = OpenseesSpringSection
        backend[StrutSection] = OpenseesStrutSection
        backend[TieSection] = OpenseesTieSection
        backend[TrapezoidalSection] = OpenseesTrapezoidalSection
        backend[TrussSection] = OpenseesTrussSection

        backend[ElasticIsotropic] = OpenseesElasticIsotropic
        backend[ElasticOrthotropic] = OpenseesElasticOrthotropic
        backend[ElasticPlastic] = OpenseesElasticPlastic
        backend[Stiff] = OpenseesStiff
        backend[UserMaterial] = OpenseesUserMaterial
        backend[Concrete] = OpenseesConcrete
        backend[ConcreteDamagedPlasticity] = OpenseesConcreteDamagedPlasticity
        backend[ConcreteSmearedCrack] = OpenseesConcreteSmearedCrack
        backend[Steel] = OpenseesSteel

        backend[NodesGroup] = OpenseesNodesGroup
        backend[ElementsGroup] = OpenseesElementsGroup
        backend[FacesGroup] = OpenseesFacesGroup

        backend[HardContactFrictionPenalty] = OpenseesHardContactFrictionPenalty

        backend[TieConstraint] = OpenseesTieConstraint

        backend[BeamEndPinRelease] = OpenseesBeamEndPinRelease

        backend[FixedBC] = OpenseesFixedBC
        backend[FixedBCXX] = OpenseesFixedBCXX
        backend[FixedBCYY] = OpenseesFixedBCYY
        backend[FixedBCZZ] = OpenseesFixedBCZZ
        backend[PinnedBC] = OpenseesPinnedBC
        backend[RollerBCX] = OpenseesRollerBCX
        backend[RollerBCXY] = OpenseesRollerBCXY
        backend[RollerBCXZ] = OpenseesRollerBCXZ
        backend[RollerBCY] = OpenseesRollerBCY
        backend[RollerBCYZ] = OpenseesRollerBCYZ
        backend[RollerBCZ] = OpenseesRollerBCZ

        backend[Problem] = OpenseesProblem

        backend[ModalAnalysis] = OpenseesModalAnalysis
        backend[ComplexEigenValue, StaticStep] = OpenseesComplexEigenValue
        backend[StaticStep] = OpenseesStaticStep
        backend[LinearStaticPerturbation] = OpenseesLinearStaticPerturbation
        backend[BucklingAnalysis] = OpenseesBucklingAnalysis
        backend[DynamicStep] = OpenseesDynamicStep
        backend[QuasiStaticStep] = OpenseesQuasiStaticStep
        backend[DirectCyclicStep] = OpenseesDirectCyclicStep

        backend[GravityLoad] = OpenseesGravityLoad
        backend[PointLoad] = OpenseesPointLoad
        backend[LineLoad] = OpenseesLineLoad
        backend[AreaLoad] = OpenseesAreaLoad
        backend[TributaryLoad] = OpenseesTributaryLoad
        backend[PrestressLoad] = OpenseesPrestressLoad
        backend[HarmonicPointLoad] = OpenseesHarmonicPointLoad
        backend[HarmonicPressureLoad] = OpenseesHarmonicPressureLoad

        backend[GeneralDisplacement] = OpenseesGeneralDisplacement

        backend[FieldOutput] = OpenseesFieldOutput
        backend[HistoryOutput] = OpenseesHistoryOutput

        backend[Results] = OpenseesResults

        backend[InputFile] = OpenseesInputFile
        backend[ParametersFile] = OpenseesParametersFile

        print('Opensees implementations registered...')
except:
    raise ErrorDuringImport()
