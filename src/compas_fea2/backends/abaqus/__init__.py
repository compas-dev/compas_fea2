"""
********************************************************************************
Abaqus
********************************************************************************
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
    TetrahedronElement,
    PentahedronElement,
    HexahedronElement,
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
#                           ABAQUS CLASSES
# =========================================================================

try:
    # Abaqus Models
    from .model import AbaqusModel
    from .model import AbaqusPart
    from .model import AbaqusNode

    # Abaqus Elements
    from .model.elements import (
        AbaqusMassElement,
        AbaqusBeamElement,
        AbaqusTrussElement,
        AbaqusMembraneElement,
        AbaqusShellElement,
        AbaqusSolidElement,
        AbaqusTetrahedonElement,
        AbaqusPentahedronElement,
        AbaqusHexahedronElement,
    )

    # Abaqus Sections
    from .model.sections import (
        AbaqusAngleSection,
        AbaqusBeamSection,
        AbaqusBoxSection,
        AbaqusCircularSection,
        AbaqusHexSection,
        AbaqusISection,
        AbaqusMassSection,
        AbaqusPipeSection,
        AbaqusRectangularSection,
        AbaqusSpringSection,
        AbaqusStrutSection,
        AbaqusTieSection,
        AbaqusTrapezoidalSection,
        AbaqusTrussSection,
        AbaqusMembraneSection,
        AbaqusShellSection,
        AbaqusSolidSection,
    )

    # Abaqus Materials
    from .model.materials import (
        AbaqusElasticIsotropic,
        AbaqusElasticOrthotropic,
        AbaqusElasticPlastic,
        AbaqusStiff,
        AbaqusUserMaterial,
        AbaqusConcrete,
        AbaqusConcreteDamagedPlasticity,
        AbaqusConcreteSmearedCrack,
        AbaqusSteel,
    )

    # Abaqus Groups
    from .model.groups import (
        AbaqusNodesGroup,
        AbaqusElementsGroup,
        AbaqusFacesGroup,
    )

    # Abaqus Interactions
    from .model.interactions import (
        AbaqusHardContactFrictionPenalty,
    )
    # Abaqus Constraints
    from .model.constraints import (
        AbaqusTieConstraint,
    )

    # Abaqus release
    from .model.releases import (
        AbaqusBeamEndPinRelease,
    )

    # Abaqus Boundary Conditions
    from .model.bcs import (
        AbaqusFixedBC,
        AbaqusFixedBCXX,
        AbaqusFixedBCYY,
        AbaqusFixedBCZZ,
        AbaqusPinnedBC,
        AbaqusRollerBCX,
        AbaqusRollerBCXY,
        AbaqusRollerBCXZ,
        AbaqusRollerBCY,
        AbaqusRollerBCYZ,
        AbaqusRollerBCZ,
    )

    # Abaqus Problem
    from .problem import AbaqusProblem

    # Abaqus Steps
    from .problem.steps import (
        AbaqusModalAnalysis,
        AbaqusComplexEigenValue,
        AbaqusStaticStep,
        AbaqusLinearStaticPerturbation,
        AbaqusBucklingAnalysis,
        AbaqusDynamicStep,
        AbaqusQuasiStaticStep,
        AbaqusDirectCyclicStep,
    )
    # Abaqus Loads
    from .problem.loads import (
        AbaqusPointLoad,
        AbaqusLineLoad,
        AbaqusAreaLoad,
        AbaqusTributaryLoad,
        AbaqusPrestressLoad,
        AbaqusGravityLoad,
        AbaqusHarmonicPointLoad,
        AbaqusHarmonicPressureLoad,
    )

    # Abaqus Displacements
    from .problem.displacements import (
        AbaqusGeneralDisplacement,
    )

    # Abaqus outputs
    from .problem.outputs import (
        AbaqusFieldOutput,
        AbaqusHistoryOutput,
    )

    # Abaqus Results
    from .results import (
        AbaqusResults
    )

    # Abaqus Input File
    from .job import(
        AbaqusInputFile,
        AbaqusParametersFile,
    )

    @plugin(category='fea_backends')
    def register_backend():
        backend = compas_fea2.BACKENDS['abaqus']

        backend[Model] = AbaqusModel
        backend[Part] = AbaqusPart
        backend[Node] = AbaqusNode

        backend[MassElement] = AbaqusMassElement
        backend[BeamElement] = AbaqusBeamElement
        backend[TrussElement] = AbaqusTrussElement
        backend[MembraneElement] = AbaqusMembraneElement
        backend[ShellElement] = AbaqusShellElement
        backend[SolidElement] = AbaqusSolidElement
        backend[SolidElement] = AbaqusSolidElement
        backend[SolidElement] = AbaqusSolidElement
        backend[TetrahedronElement] = AbaqusTetrahedonElement
        backend[PentahedronElement] = AbaqusPentahedronElement
        backend[HexahedronElement] = AbaqusHexahedronElement

        backend[AngleSection] = AbaqusAngleSection
        backend[BeamSection] = AbaqusBeamSection
        backend[BoxSection] = AbaqusBoxSection
        backend[CircularSection] = AbaqusCircularSection
        backend[HexSection] = AbaqusHexSection
        backend[ISection] = AbaqusISection
        backend[MassSection] = AbaqusMassSection
        backend[MembraneSection] = AbaqusMembraneSection
        backend[PipeSection] = AbaqusPipeSection
        backend[RectangularSection] = AbaqusRectangularSection
        backend[ShellSection] = AbaqusShellSection
        backend[SolidSection] = AbaqusSolidSection
        backend[SpringSection] = AbaqusSpringSection
        backend[StrutSection] = AbaqusStrutSection
        backend[TieSection] = AbaqusTieSection
        backend[TrapezoidalSection] = AbaqusTrapezoidalSection
        backend[TrussSection] = AbaqusTrussSection

        backend[ElasticIsotropic] = AbaqusElasticIsotropic
        backend[ElasticOrthotropic] = AbaqusElasticOrthotropic
        backend[ElasticPlastic] = AbaqusElasticPlastic
        backend[Stiff] = AbaqusStiff
        backend[UserMaterial] = AbaqusUserMaterial
        backend[Concrete] = AbaqusConcrete
        backend[ConcreteDamagedPlasticity] = AbaqusConcreteDamagedPlasticity
        backend[ConcreteSmearedCrack] = AbaqusConcreteSmearedCrack
        backend[Steel] = AbaqusSteel

        backend[NodesGroup] = AbaqusNodesGroup
        backend[ElementsGroup] = AbaqusElementsGroup
        backend[FacesGroup] = AbaqusFacesGroup

        backend[HardContactFrictionPenalty] = AbaqusHardContactFrictionPenalty

        backend[TieConstraint] = AbaqusTieConstraint

        backend[BeamEndPinRelease] = AbaqusBeamEndPinRelease

        backend[FixedBC] = AbaqusFixedBC
        backend[FixedBCXX] = AbaqusFixedBCXX
        backend[FixedBCYY] = AbaqusFixedBCYY
        backend[FixedBCZZ] = AbaqusFixedBCZZ
        backend[PinnedBC] = AbaqusPinnedBC
        backend[RollerBCX] = AbaqusRollerBCX
        backend[RollerBCXY] = AbaqusRollerBCXY
        backend[RollerBCXZ] = AbaqusRollerBCXZ
        backend[RollerBCY] = AbaqusRollerBCY
        backend[RollerBCYZ] = AbaqusRollerBCYZ
        backend[RollerBCZ] = AbaqusRollerBCZ

        backend[Problem] = AbaqusProblem

        backend[ModalAnalysis] = AbaqusModalAnalysis
        backend[ComplexEigenValue, StaticStep] = AbaqusComplexEigenValue
        backend[StaticStep] = AbaqusStaticStep
        backend[LinearStaticPerturbation] = AbaqusLinearStaticPerturbation
        backend[BucklingAnalysis] = AbaqusBucklingAnalysis
        backend[DynamicStep] = AbaqusDynamicStep
        backend[QuasiStaticStep] = AbaqusQuasiStaticStep
        backend[DirectCyclicStep] = AbaqusDirectCyclicStep

        backend[GravityLoad] = AbaqusGravityLoad
        backend[PointLoad] = AbaqusPointLoad
        backend[LineLoad] = AbaqusLineLoad
        backend[AreaLoad] = AbaqusAreaLoad
        backend[TributaryLoad] = AbaqusTributaryLoad
        backend[PrestressLoad] = AbaqusPrestressLoad
        backend[HarmonicPointLoad] = AbaqusHarmonicPointLoad
        backend[HarmonicPressureLoad] = AbaqusHarmonicPressureLoad

        backend[GeneralDisplacement] = AbaqusGeneralDisplacement

        backend[FieldOutput] = AbaqusFieldOutput
        backend[HistoryOutput] = AbaqusHistoryOutput

        backend[Results] = AbaqusResults

        backend[InputFile] = AbaqusInputFile
        backend[ParametersFile] = AbaqusParametersFile

        print('Abaqus implementations registered...')
except:
    raise ErrorDuringImport()
