#! /usr/bin/env python3
#
def trapezoidal ( f, tspan, y0, n ):

#*****************************************************************************80
#
## trapezoidal() uses trapezoidal + fsolve to solve an ODE.
#
#  Licensing:
#
#    This code is distributed under the MIT license.
#
#  Modified:
#
#    22 October 2020
#
#  Author:
#
#    John Burkardt
#
#  Input:
#
#    function f: evaluates the right hand side of the ODE.  
#
#    real tspan[2]: the starting and ending times.
#
#    real y0[m]: the initial conditions. 
#
#    integer n: the number of steps.
#
#  Output:
#
#    real t[n+1], y[n+1,m]: the solution estimates.
#
  from scipy.optimize import fsolve
  import numpy as np

  if ( np.ndim ( y0 ) == 0 ):
    m = 1
  else:
    m = len ( y0 )

  t = np.zeros ( n + 1 )
  y = np.zeros ( [ n + 1, m ] )

  dt = ( tspan[1] - tspan[0] ) / float ( n )

  t[0] = 0.0
  y[0,:] = y0

  for i in range ( 0, n ):

    to = t[i]
    yo = y[i,:]

    tn = t[i] + dt
    yn = y[i,:] + dt * f ( to, yo )

    yn = fsolve ( trapezoidal_residual, yn, args = ( f, to, yo, tn ) )

    t[i+1]   = tn
    y[i+1,:] = yn[:]

  return t, y

def trapezoidal_residual ( yn, f, to, yo, tn ):

#*****************************************************************************80
#
## trapezoidal_residual() evaluates the trapezoidal residual.
#
#  Discussion:
#
#    We are seeking a value YN defined by the implicit equation:
#
#      YN = YO + 0.5 * ( TN - TO ) * ( F ( TO, YO ) + F ( TN, YN ) )
#
#  Licensing:
#
#    This code is distributed under the MIT license.
#
#  Modified:
#
#    22 October 2020
#
#  Author:
#
#    John Burkardt
#
#  Input:
#
#    real yn: the estimated solution value at the new time.
#
#    function f: evaluates the right hand side of the ODE.  
#
#    real to, yo: the old time and solution value.
#
#    real tn: the new time.
#
#  Output:
#
#    real value: the trapezoidal residual.
#
  value = yn - yo - ( tn - to ) * ( f ( to, yo ) + f ( tn, yn ) );

  return value

def trapezoidal_test ( ):

#*****************************************************************************80
#
## trapezoidal_test() tests trapezoidal.
#
#  Licensing:
#
#    This code is distributed under the MIT license. 
#
#  Modified:
#
#    26 April 2021
#
#  Author:
#
#    John Burkardt
#
  import numpy as np
  import platform

  print ( '' )
  print ( 'trapezoidal_test:' )
  print ( '  Python version: %s' % ( platform.python_version ( ) ) )
  print ( '  Test trapezoidal()' )

  tspan = np.array ( [ 0.0, 2.0 ] )
  y0 = 5.1765
  n = 100
  humps_trapezoidal ( tspan, y0, n )

  tspan = np.array ( [ 0.0, 5.0 ] )
  y0 = np.array ( [ 5000, 100 ] )
  n = 200
  predator_prey_trapezoidal ( tspan, y0, n )
#
#  Terminate.
#
  print ( '' )
  print ( 'trapezoidal_test:' )
  print ( '  Normal end of execution.' )
  return

def humps_trapezoidal ( tspan, y0, n ):

#*****************************************************************************80
#
## humps_trapezoidal(): humps ODE using trapezoidal_fsolve().
#
#  Licensing:
#
#    This code is distributed under the MIT license.
#
#  Modified:
#
#    22 October 2020
#
#  Author:
#
#    John Burkardt
#
#  Input:
#
#    real tspan[2]: the time span
#
#    real y0[2]: the initial condition.
#
#    integer n: the number of steps to take.
#
  import matplotlib.pyplot as plt
  import numpy as np

  print ( '' )
  print ( 'humps_trapezoidal:' )
  print ( '  Solve the humps ODE system using trapezoidal_fsolve().' )

  t, y = trapezoidal ( humps_deriv, tspan, y0, n )

  plt.plot ( t, y, 'r-', linewidth = 2 )

  a = tspan[0]
  b = tspan[1]
  if ( a <= 0.0 and 0.0 <= b ):
    plt.plot ( [a,b], [0,0], 'k-', linewidth = 2 )

  ymin = min ( y )
  ymax = max ( y )
  if ( ymin <= 0.0 and 0.0 <= ymax ):
    plt.plot ( [0, 0], [ymin,ymax], 'k-', linewidth = 2 )

  plt.grid ( True )
  plt.xlabel ( '<--- T --->' )
  plt.ylabel ( '<--- Y(T) --->' )
  plt.title ( 'humps ODE solved by trapezoidal()' )

  filename = 'humps_trapezoidal.png'
  plt.savefig ( filename )
  print ( '  Graphics saved as "%s"' % ( filename ) )
  plt.show ( block = False )
  plt.close ( )

  return

def predator_prey_trapezoidal ( tspan, y0, n ):

#*****************************************************************************80
#
## predator_prey_trapezoidal: predator ODE using trapezoidal().
#
#  Licensing:
#
#    This code is distributed under the MIT license.
#
#  Modified:
#
#    22 October 2020
#
#  Author:
#
#    John Burkardt
#
#  Input:
#
#    real tspan[2]: the time span
#
#    real y0[2]: the initial condition.
#
#    integer n: the number of steps to take.
#
  import matplotlib.pyplot as plt
  import numpy as np

  print ( '' )
  print ( 'predator_prey_trapezoidal:' )
  print ( '  Solve the predator prey ODE system using trapezoidal().' )

  t, y = trapezoidal ( predator_prey_deriv, tspan, y0, n )

  plt.plot ( y[:,0], y[:,1], 'r-', linewidth = 2 )

  plt.grid ( True )
  plt.xlabel ( '<--- Prey --->' )
  plt.ylabel ( '<--- Predators --->' )
  plt.title ( 'predator prey ODE solved by trapezoidal' )

  filename = 'predator_prey_trapezoidal.png'
  plt.savefig ( filename )
  print ( '  Graphics saved as "%s"' % ( filename ) )
  plt.show ( block = False )
  plt.close ( )

  return

def humps_deriv ( x, y ):

#*****************************************************************************80
#
## humps_deriv() evaluates the derivative of the humps function.
#
#  Discussion:
#
#    y = 1.0 ./ ( ( x - 0.3 )^2 + 0.01 ) 
#      + 1.0 ./ ( ( x - 0.9 )^2 + 0.04 ) 
#      - 6.0
#
#  Licensing:
#
#    This code is distributed under the MIT license.
#
#  Modified:
#
#    22 April 2020
#
#  Author:
#
#    John Burkardt
#
#  Input:
#
#    real x[:], y[:]: the arguments.
#
#  Output:
#
#    real yp[:]: the value of the derivative at x.
#
  yp = - 2.0 * ( x - 0.3 ) / ( ( x - 0.3 )**2 + 0.01 )**2 \
       - 2.0 * ( x - 0.9 ) / ( ( x - 0.9 )**2 + 0.04 )**2

  return yp

def predator_prey_deriv ( t, rf ):

#*****************************************************************************80
#
## predator_prey_deriv() evaluates the right hand side of the system.
#
#  Licensing:
#
#    This code is distributed under the MIT license.
#
#  Modified:
#
#    22 April 2020
#
#  Author:
#
#    John Burkardt
#
#  Reference:
#
#    George Lindfield, John Penny,
#    Numerical Methods Using MATLAB,
#    Second Edition,
#    Prentice Hall, 1999,
#    ISBN: 0-13-012641-1,
#    LC: QA297.P45.
#
#  Input:
#
#    real T, the current time.
#
#    real RF[2], the current solution variables, rabbits and foxes.
#
#  Output:
#
#    real DRFDT[2], the right hand side of the 2 ODE's.
#
  import numpy as np

  r = rf[0]
  f = rf[1]

  drdt =    2.0 * r - 0.001 * r * f
  dfdt = - 10.0 * f + 0.002 * r * f

  drfdt = np.array ( [ drdt, dfdt ] )

  return drfdt

def timestamp ( ):

#*****************************************************************************80
#
## timestamp() prints the date as a timestamp.
#
#  Licensing:
#
#    This code is distributed under the MIT license. 
#
#  Modified:
#
#    21 August 2019
#
#  Author:
#
#    John Burkardt
#
  import time

  t = time.time ( )
  print ( time.ctime ( t ) )

  return

if ( __name__ == '__main__' ):
  timestamp ( )
  trapezoidal_test ( )
  timestamp ( )
