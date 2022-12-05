"""
********************************************************************************
Sofistik
********************************************************************************
"""

from pydoc import ErrorDuringImport
import compas_fea2

from compas.plugins import plugin

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
    Timber,
)

# Boundary Conditions
from compas_fea2.model.bcs import (
    GeneralBC,
    FixedBC,
    ClampBCXX,
    ClampBCYY,
    ClampBCZZ,
    PinnedBC,
    RollerBCX,
    RollerBCXY,
    RollerBCXZ,
    RollerBCY,
    RollerBCYZ,
    RollerBCZ,
)

# Constraints
from compas_fea2.model.constraints import (
    TieMPC,
    BeamMPC,
    TieConstraint,
)

# Intial Conditions
from compas_fea2.model.ics import (
    InitialTemperatureField,
    InitialStressField,
)

# Elements
from compas_fea2.model.elements import (
    MassElement,
    BeamElement,
    TrussElement,
    MembraneElement,
    ShellElement,
    _Element3D,
    TetrahedronElement,
    HexahedronElement,
)

# Groups
from compas_fea2.model.groups import (
    NodesGroup,
    ElementsGroup,
    FacesGroup,
)

# Models
from compas_fea2.model import Model

# Nodes
from compas_fea2.model import Node

# Parts
from compas_fea2.model import DeformablePart, RigidPart

# Releases
from compas_fea2.model.releases import (
    BeamEndPinRelease,
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
# Displacements
from compas_fea2.problem.displacements import (
    GeneralDisplacement,
)
# Fields
from compas_fea2.problem.fields import (
    PrescribedTemperatureField,
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
    ThermalLoad
)

# Outputs
from compas_fea2.problem.outputs import (
    FieldOutput,
    HistoryOutput,
)

# Problem
from compas_fea2.problem import Problem

# Results
from compas_fea2.results import (
    Results,
    StepResults,
)

# Input File
from compas_fea2.job import (
    InputFile,
    ParametersFile,
)
# =========================================================================
#                           SOFISTIK CLASSES
# =========================================================================

try:
    # Sofistik Models
    from .model import SofistikModel
    from .model import SofistikDeformablePart, SofistikRigidPart
    from .model import SofistikNode

    # Sofistik Elements
    from .model.elements import (
        SofistikMassElement,
        SofistikBeamElement,
        SofistikTrussElement,
        SofistikMembraneElement,
        SofistikShellElement,
        _SofistikElement3D,
        SofistikTetrahedronElement,
        SofistikHexahedronElement,
    )

    # Sofistik Sections
    from .model.sections import (
        SofistikAngleSection,
        SofistikBeamSection,
        SofistikBoxSection,
        SofistikCircularSection,
        SofistikHexSection,
        SofistikISection,
        SofistikMassSection,
        SofistikPipeSection,
        SofistikRectangularSection,
        SofistikSpringSection,
        SofistikStrutSection,
        SofistikTieSection,
        SofistikTrapezoidalSection,
        SofistikTrussSection,
        SofistikMembraneSection,
        SofistikShellSection,
        SofistikSolidSection,
    )

    # Sofistik Materials
    from .model.materials import (
        SofistikElasticIsotropic,
        SofistikElasticOrthotropic,
        SofistikElasticPlastic,
        SofistikStiff,
        SofistikUserMaterial,
        SofistikConcrete,
        SofistikConcreteDamagedPlasticity,
        SofistikConcreteSmearedCrack,
        SofistikSteel,
        SofistikTimber,
    )

    # Sofistik Groups
    from .model.groups import (
        SofistikNodesGroup,
        SofistikElementsGroup,
        SofistikFacesGroup,
    )

    # Sofistik Constraints
    from .model.constraints import (
        SofistikTieMPC,
        SofistikBeamMPC,
        SofistikTieConstraint,
    )

    # Sofistik Initial Conditions
    from .model.ics import (
        SofistikInitialTemperatureField,
        SofistikInitialStressField,
    )

    # Sofistik release
    from .model.releases import (
        SofistikBeamEndPinRelease,
    )

    # Sofistik Boundary Conditions
    from .model.bcs import (
        SofistikGeneralBC,
        SofistikFixedBC,
        SofistikClampBCXX,
        SofistikClampBCYY,
        SofistikClampBCZZ,
        SofistikPinnedBC,
        SofistikRollerBCX,
        SofistikRollerBCXY,
        SofistikRollerBCXZ,
        SofistikRollerBCY,
        SofistikRollerBCYZ,
        SofistikRollerBCZ,
    )

    # Sofistik Problem
    from .problem import SofistikProblem

    # Sofistik Steps
    from .problem.steps import (
        SofistikModalAnalysis,
        SofistikComplexEigenValue,
        SofistikStaticStep,
        SofistikLinearStaticPerturbation,
        SofistikBucklingAnalysis,
        SofistikDynamicStep,
        SofistikQuasiStaticStep,
        SofistikDirectCyclicStep,
    )
    # Sofistik Loads
    from .problem.loads import (
        SofistikPointLoad,
        SofistikLineLoad,
        SofistikAreaLoad,
        SofistikTributaryLoad,
        SofistikPrestressLoad,
        SofistikGravityLoad,
        SofistikHarmonicPointLoad,
        SofistikHarmonicPressureLoad,
        SofistikThermalLoad,
    )

    # Sofistik Fields
    from .problem.fields import (
        SofistikPrescribedTemperatureField,
    )

    # Sofistik Displacements
    from .problem.displacements import (
        SofistikGeneralDisplacement,
    )

    # Sofistik outputs
    from .problem.outputs import (
        SofistikFieldOutput,
        SofistikHistoryOutput,
    )

    # Sofistik Results
    from .results import (
        SofistikResults,
        SofistikStepResults,
    )

    # Sofistik Input File
    from .job import(
        SofistikInputFile,
        SofistikParametersFile,
    )

    @plugin(category='fea_backends')
    def register_backend():
        backend = compas_fea2.BACKENDS['sofistik']

        backend[Model] = SofistikModel

        backend[DeformablePart] = SofistikDeformablePart
        backend[RigidPart] = SofistikRigidPart

        backend[Node] = SofistikNode

        backend[MassElement] = SofistikMassElement
        backend[BeamElement] = SofistikBeamElement
        backend[TrussElement] = SofistikTrussElement
        backend[MembraneElement] = SofistikMembraneElement
        backend[ShellElement] = SofistikShellElement
        backend[TetrahedronElement] = SofistikTetrahedronElement
        backend[HexahedronElement] = SofistikHexahedronElement

        backend[AngleSection] = SofistikAngleSection
        backend[BeamSection] = SofistikBeamSection
        backend[BoxSection] = SofistikBoxSection
        backend[CircularSection] = SofistikCircularSection
        backend[HexSection] = SofistikHexSection
        backend[ISection] = SofistikISection
        backend[MassSection] = SofistikMassSection
        backend[MembraneSection] = SofistikMembraneSection
        backend[PipeSection] = SofistikPipeSection
        backend[RectangularSection] = SofistikRectangularSection
        backend[ShellSection] = SofistikShellSection
        backend[SolidSection] = SofistikSolidSection
        backend[SpringSection] = SofistikSpringSection
        backend[StrutSection] = SofistikStrutSection
        backend[TieSection] = SofistikTieSection
        backend[TrapezoidalSection] = SofistikTrapezoidalSection
        backend[TrussSection] = SofistikTrussSection

        backend[ElasticIsotropic] = SofistikElasticIsotropic
        backend[ElasticOrthotropic] = SofistikElasticOrthotropic
        backend[ElasticPlastic] = SofistikElasticPlastic
        backend[Stiff] = SofistikStiff
        backend[UserMaterial] = SofistikUserMaterial
        backend[Concrete] = SofistikConcrete
        backend[ConcreteDamagedPlasticity] = SofistikConcreteDamagedPlasticity
        backend[ConcreteSmearedCrack] = SofistikConcreteSmearedCrack
        backend[Steel] = SofistikSteel
        backend[Timber] = SofistikTimber

        backend[NodesGroup] = SofistikNodesGroup
        backend[ElementsGroup] = SofistikElementsGroup
        backend[FacesGroup] = SofistikFacesGroup

        backend[TieMPC] = SofistikTieMPC
        backend[BeamMPC] = SofistikBeamMPC
        backend[TieConstraint] = SofistikTieConstraint

        backend[BeamEndPinRelease] = SofistikBeamEndPinRelease

        backend[InitialTemperatureField] = SofistikInitialTemperatureField
        backend[InitialStressField] = SofistikInitialStressField

        backend[GeneralBC] = SofistikGeneralBC
        backend[FixedBC] = SofistikFixedBC
        backend[ClampBCXX] = SofistikClampBCXX
        backend[ClampBCYY] = SofistikClampBCYY
        backend[ClampBCZZ] = SofistikClampBCZZ
        backend[PinnedBC] = SofistikPinnedBC
        backend[RollerBCX] = SofistikRollerBCX
        backend[RollerBCXY] = SofistikRollerBCXY
        backend[RollerBCXZ] = SofistikRollerBCXZ
        backend[RollerBCY] = SofistikRollerBCY
        backend[RollerBCYZ] = SofistikRollerBCYZ
        backend[RollerBCZ] = SofistikRollerBCZ

        backend[Problem] = SofistikProblem

        backend[ModalAnalysis] = SofistikModalAnalysis
        backend[ComplexEigenValue, StaticStep] = SofistikComplexEigenValue
        backend[StaticStep] = SofistikStaticStep
        backend[LinearStaticPerturbation] = SofistikLinearStaticPerturbation
        backend[BucklingAnalysis] = SofistikBucklingAnalysis
        backend[DynamicStep] = SofistikDynamicStep
        backend[QuasiStaticStep] = SofistikQuasiStaticStep
        backend[DirectCyclicStep] = SofistikDirectCyclicStep

        backend[GravityLoad] = SofistikGravityLoad
        backend[PointLoad] = SofistikPointLoad
        backend[LineLoad] = SofistikLineLoad
        backend[AreaLoad] = SofistikAreaLoad
        backend[TributaryLoad] = SofistikTributaryLoad
        backend[PrestressLoad] = SofistikPrestressLoad
        backend[HarmonicPointLoad] = SofistikHarmonicPointLoad
        backend[HarmonicPressureLoad] = SofistikHarmonicPressureLoad
        backend[ThermalLoad] = SofistikThermalLoad

        backend[GeneralDisplacement] = SofistikGeneralDisplacement

        backend[PrescribedTemperatureField] = SofistikPrescribedTemperatureField

        backend[FieldOutput] = SofistikFieldOutput
        backend[HistoryOutput] = SofistikHistoryOutput

        backend[Results] = SofistikResults
        backend[StepResults] = SofistikStepResults

        backend[InputFile] = SofistikInputFile
        backend[ParametersFile] = SofistikParametersFile

        print('Sofistik implementations registered...')
except:
    raise ErrorDuringImport()
