/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/18 22:59:13 by tsellak           #+#    #+#             */
/*   Updated: 2025/10/29 02:39:26 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memchr(const void *s, int c, size_t n)
{
	unsigned char	*str;
	unsigned char	c_c;
	size_t			i;

	str = (unsigned char *)s;
	c_c = (unsigned char)c;
	i = 0;
	while (i < n)
	{
		if (str[i] == c_c)
			return (&str[i]);
		i++;
	}
	return (NULL);
}
