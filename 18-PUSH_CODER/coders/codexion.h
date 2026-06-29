/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/29 08:52:42 by Tsellak           #+#    #+#             */
/*   Updated: 2026/06/29 10:36:33 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <limits.h>
# include <pthread.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <sys/time.h>
# include <time.h>
# include <unistd.h>

typedef struct s_coder
{
	int				id;
	pthread_t		thread;
	long			last_compile_start;
	long			deadline;
	int				compile_count;
	int				left_dongle;
	int				right_dongle;
	struct s_data	*data;
	pthread_mutex_t	state_mutex;
}					t_coder;

typedef struct s_dongle
{
	pthread_mutex_t	mutex;
	pthread_cond_t	cond;
	int				in_use;
	long			release_time;
	t_coder			**queue;
	int				tail;
}					t_dongle;

typedef struct s_data
{
	int				num_coders;
	long			time_to_burnout;
	long			time_to_compile;
	long			time_to_debug;
	long			time_to_refactor;
	int				num_compiles_required;
	long			dongle_cooldown;
	int				scheduler;
	long			start_time;
	int				simulation_end;
	t_dongle		*dongles;
	t_coder			*coders;
	pthread_t		monitor;
	pthread_mutex_t	print_mutex;
	pthread_mutex_t	state_mutex;
}					t_data;

// logger
void				ft_exit(const char *format, const void *arg1,
						const void *arg2);
void				log_action(t_coder *coder, const char *message);

// time utils
long				get_time_ms(void);
void				ms_to_timespec(struct timespec *ts, long ms);
long				get_next_timeout(t_coder *coder, t_dongle *dongle);
int					sleep_until_or_burnout(t_coder *coder, long duration_ms);

// coder
void				*coder_routine(void *arg);

// monitor
int					simulation_check(t_data *data);
int					mark_burnout(t_coder *coder);
void				*monitor_routine(void *arg);

// dongle
int					take_two_dongles(t_coder *coder);
void				release_two_dongles(t_coder *coder);

// init
int					start_threads(t_data *data);

// cleanup
void				cleanup_all(t_data *data);

// main
long				ft_atol(char *str);

// heap + scheduler
void				queue_push(t_dongle *dongle, t_coder *coder);
t_coder				*queue_pop(t_dongle *dongle, t_data *data);
void				queue_remove(t_dongle *dongle, t_coder *coder);
int					compare_edf(t_coder *a, t_coder *b);
void				heap_up(t_dongle *dongle);
void				heap_down(t_dongle *dongle);

#endif
